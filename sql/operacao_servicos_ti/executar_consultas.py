"""Executa 10 perguntas de negócio e atualiza um resumo com dados sintéticos."""
from __future__ import annotations

import sqlite3
from pathlib import Path

PASTA = Path(__file__).resolve().parent
BANCO = PASTA / "operacao_exemplo.sqlite"
QUESTOES = [
    ("01_volume_por_equipe.sql", "Volume por equipe", "Qual equipe concentra mais chamados?"),
    ("02_perfil_de_prioridades.sql", "Perfil de prioridades", "Qual é o perfil das prioridades em cada serviço?"),
    ("03_cumprimento_sla.sql", "Cumprimento de SLA", "Quais serviços têm maior incidência de chamados fora da meta?"),
    ("04_tendencia_mensal.sql", "Evolução mensal", "O volume de chamados aumentou ou diminuiu?"),
    ("05_ranking_violacao_sla.sql", "Ranking de violações de SLA", "Onde estão concentradas as ocorrências fora do prazo?"),
    ("06_backlog_por_idade.sql", "Backlog por idade", "Qual é o envelhecimento dos chamados ainda abertos?"),
    ("07_satisfacao_e_sla.sql", "Avaliações e SLA", "Como variam as notas dos chamados dentro e fora da meta?"),
    ("08_pareto_servicos.sql", "Concentração por serviço", "Quais serviços respondem pela maior parte da demanda?"),
    ("09_media_movel_diaria.sql", "Média móvel de sete dias", "Como varia a demanda diária ao longo do tempo?"),
    ("10_plano_e_indices.sql", "Plano de execução e índices", "Qual plano o banco escolhe para a consulta filtrada?"),
]


def consultar(conn: sqlite3.Connection, nome: str) -> tuple[list[str], list[tuple]]:
    sql = (PASTA / "consultas" / nome).read_text(encoding="utf-8")
    cursor = conn.execute(sql)
    return [c[0] for c in cursor.description], cursor.fetchall()


def tabela_md(colunas: list[str], linhas: list[tuple], max_linhas: int = 6) -> str:
    def seguro(v: object) -> str:
        return "—" if v is None else str(v).replace("|", "\\|")
    cab = "| " + " | ".join(colunas) + " |"
    sep = "| " + " | ".join("---" for _ in colunas) + " |"
    corpo = ["| " + " | ".join(seguro(x) for x in row) + " |" for row in linhas[:max_linhas]]
    if len(linhas) > max_linhas:
        corpo.append(f"*Exibindo {max_linhas} de {len(linhas)} linhas.*")
    return "\n".join([cab, sep, *corpo])


def grafico_mensal(linhas: list[tuple]) -> None:
    # SVG legível no GitHub, produzido somente de agregações dos dados fictícios.
    valores = [(row[0], row[1]) for row in linhas]
    maximo = max(v for _, v in valores)
    partes = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 790 365" role="img">',
        '<title>Volume mensal de chamados simulados</title>',
        '<rect width="790" height="365" fill="#ffffff"/>',
        '<text x="26" y="40" font-family="Arial" font-size="23" font-weight="bold" fill="#18324b">',
        'Chamados por mês — dados fictícios</text>',
        '<text x="26" y="65" font-family="Arial" font-size="14" fill="#54667a">',
        'Demonstração de agregação SQL e evolução temporal</text>',
    ]
    largura = 102
    espacamento = 65
    for i, (mes, total) in enumerate(valores):
        x = 76 + i * (largura + espacamento)
        altura = 220 * total / maximo
        y = 298 - altura
        partes.append(f'<rect x="{x}" y="{y:.1f}" width="{largura}" height="{altura:.1f}" rx="5" fill="#16818b"/>')
        partes.append(f'<text x="{x + largura / 2:.1f}" y="{y - 10:.1f}" text-anchor="middle" font-family="Arial" font-size="16" fill="#18324b">{total}</text>')
        partes.append(f'<text x="{x + largura / 2:.1f}" y="325" text-anchor="middle" font-family="Arial" font-size="14" fill="#54667a">{mes}</text>')
    partes.append('</svg>')
    (PASTA / "figuras" / "volume_mensal.svg").write_text("".join(partes), encoding="utf-8")


def gerar_relatorio() -> dict[str, int]:
    if not BANCO.exists():
        raise FileNotFoundError("Execute primeiro: python gerar_base.py")
    contagens = {}
    with sqlite3.connect(f"file:{BANCO}?mode=ro", uri=True) as conn:
        conn.execute("PRAGMA query_only = ON")
        qtd_chamados = conn.execute("SELECT COUNT(*) FROM chamados").fetchone()[0]
        qtd_abertos = conn.execute("SELECT COUNT(*) FROM chamados WHERE status='Aberto'").fetchone()[0]
        total_avaliacoes = conn.execute("SELECT COUNT(*) FROM avaliacoes").fetchone()[0]
        rel = [
            "# Resultados — base 100% fictícia",
            "",
            "Resultados obtidos **executando as 10 consultas SQL** sobre dados sintéticos gerados localmente.",
            "Não são indicadores reais de uma organização. Os valores servem para demonstrar consultas, leitura de dados e raciocínio analítico.",
            "",
            f"**Escala:** {qtd_chamados} chamados simulados; {qtd_abertos} abertos no corte de 01/10/2026; {total_avaliacoes} avaliações associadas.",
            "",
        ]
        for nome, titulo, pergunta in QUESTOES:
            cols, rows = consultar(conn, nome)
            contagens[nome] = len(rows)
            rel.extend([f"## {titulo}", "", f"**Pergunta:** {pergunta}", "", tabela_md(cols, rows), ""])
            if nome == "04_tendencia_mensal.sql":
                grafico_mensal(rows)
                rel.extend(["![Volume mensal fictício](figuras/volume_mensal.svg)", ""])
            if nome == "07_satisfacao_e_sla.sql":
                rel.extend(["**Interpretação:** a diferença entre grupos é descritiva e não prova causalidade; a amostra considera apenas chamados avaliados.", ""])
        rel.extend([
            "## Leitura dos resultados", "",
            "- **SLA:** a taxa usa somente chamados resolvidos; chamados abertos compõem o backlog e não o denominador de cumprimento.",
            "- **Períodos:** datas e janelas pertencem exclusivamente à simulação de junho a setembro de 2026.",
            "- **Plano de execução:** o resultado do `EXPLAIN QUERY PLAN` pode variar conforme a versão do SQLite e o tamanho da base.",
            "- **Escopo:** os exemplos demonstram consultas e comunicação de indicadores, sem substituir sistemas operacionais, políticas de segurança ou um banco de produção.",
        ])
    (PASTA / "RESULTADOS.md").write_text("\n".join(rel) + "\n", encoding="utf-8")
    return contagens


if __name__ == "__main__":
    d = gerar_relatorio()
    print("10 consultas executadas; linhas retornadas por consulta:")
    for k, v in d.items():
        print(f"  {k}: {v}")
    print("Resumo: RESULTADOS.md")
