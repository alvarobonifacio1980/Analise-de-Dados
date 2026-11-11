"""Gera banco SQLite inteiramente fictício e determinístico; sem dependências externas."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import random
import sqlite3

PASTA = Path(__file__).resolve().parent
DATA_CORTE = datetime(2026, 10, 1, 0, 0, 0)
INICIO = datetime(2026, 6, 1, 0, 0, 0)

EQUIPES = [(1, "Sistemas"), (2, "Plataformas"), (3, "Integrações"), (4, "Operações")]
SERVICOS = [
    (1, 1, "Portal de Atendimento", "Alta"),
    (2, 1, "Cadastro Digital", "Média"),
    (3, 2, "Autenticação", "Alta"),
    (4, 2, "Armazenamento", "Média"),
    (5, 3, "Integração de Aplicações", "Alta"),
    (6, 3, "Mensageria", "Média"),
    (7, 4, "Monitoramento", "Média"),
    (8, 4, "Portal Interno", "Baixa"),
]
METAS = {"P1": 120, "P2": 480, "P3": 1440, "P4": 2880}


def texto_data(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def gerar(destino: Path) -> dict[str, int]:
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        raise FileExistsError(
            f"Arquivo já existe: {destino}. Para regenerar o exemplo, remova apenas este banco sintético."
        )
    rnd = random.Random(20261111)
    with sqlite3.connect(destino) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript((PASTA / "esquema.sql").read_text(encoding="utf-8"))
        conn.executemany("INSERT INTO equipes VALUES (?, ?)", EQUIPES)
        conn.executemany("INSERT INTO servicos VALUES (?, ?, ?, ?)", SERVICOS)
        chamados = []
        avaliacoes = []
        dia = INICIO
        ident = 0
        while dia < DATA_CORTE:
            # Ao menos um chamado por dia: média móvel sobre datas consecutivas.
            qtd = rnd.randint(7, 16)
            for _ in range(qtd):
                ident += 1
                sid = rnd.choices(range(1, 9), weights=[19, 13, 15, 11, 16, 12, 8, 6])[0]
                prioridade = rnd.choices(["P1", "P2", "P3", "P4"], weights=[9, 23, 46, 22])[0]
                canal = rnd.choices(["Portal", "E-mail", "Telefone"], weights=[65, 25, 10])[0]
                abertura = dia + timedelta(hours=rnd.randrange(7, 19), minutes=rnd.randrange(60))
                # Tempos parcialmente correlacionados à meta, com cauda de atraso.
                fator = rnd.lognormvariate(-0.15, 0.67) * (1.15 if sid in (1, 5) else 0.9)
                tempo = max(5, round(METAS[prioridade] * fator))
                resolvido_em = abertura + timedelta(minutes=tempo)
                # Jamais gerar encerramento depois do recorte da análise.
                ainda_aberto = resolvido_em >= DATA_CORTE or rnd.random() < (0.035 if dia < DATA_CORTE - timedelta(days=14) else 0.12)
                if ainda_aberto:
                    status, encerramento = "Aberto", None
                else:
                    status, encerramento = "Resolvido", texto_data(resolvido_em)
                chamados.append((ident, sid, prioridade, canal, status, texto_data(abertura), encerramento))
                if not ainda_aberto and rnd.random() < 0.62:
                    nota = rnd.choices([1, 2, 3, 4, 5], weights=[15, 13, 20, 28, 24] if tempo > METAS[prioridade] else [4, 8, 16, 35, 37])[0]
                    avaliacoes.append((len(avaliacoes) + 1, ident, nota))
            dia += timedelta(days=1)
        conn.executemany("INSERT INTO chamados VALUES (?, ?, ?, ?, ?, ?, ?)", chamados)
        conn.executemany("INSERT INTO avaliacoes VALUES (?, ?, ?)", avaliacoes)
        conn.execute("ANALYZE")
        conn.commit()
        return {"equipes": len(EQUIPES), "servicos": len(SERVICOS), "chamados": len(chamados), "avaliacoes": len(avaliacoes)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera um exemplo sintético de gestão de serviços de TI")
    parser.add_argument("--saida", type=Path, default=PASTA / "operacao_exemplo.sqlite")
    args = parser.parse_args()
    contagens = gerar(args.saida.resolve())
    print("Base sintética criada:", contagens)
    print("Arquivo:", args.saida)
