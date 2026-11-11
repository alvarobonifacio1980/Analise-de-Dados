"""Verificações de integridade dos dados, consultas e totais; nenhuma dependência externa."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from gerar_base import gerar
from executar_consultas import PASTA, QUESTOES, consultar


class TesteCaseSQL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.banco = Path(cls.temp.name) / "teste.sqlite"
        cls.resumo = gerar(cls.banco)
        cls.conn = sqlite3.connect(cls.banco)
        cls.conn.execute("PRAGMA foreign_keys = ON")

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        cls.temp.cleanup()

    def test_quantidades_esperadas(self):
        self.assertEqual(self.resumo["equipes"], 4)
        self.assertEqual(self.resumo["servicos"], 8)
        self.assertGreater(self.resumo["chamados"], 1000)
        self.assertGreater(self.resumo["avaliacoes"], 100)

    def test_chaves_estrangeiras(self):
        self.assertEqual(self.conn.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_sem_datas_futuras(self):
        n = self.conn.execute("""SELECT COUNT(*) FROM chamados
            WHERE aberto_em >= '2026-10-01 00:00:00'
               OR (encerrado_em IS NOT NULL AND encerrado_em >= '2026-10-01 00:00:00')
               OR (encerrado_em IS NOT NULL AND encerrado_em < aberto_em)
        """).fetchone()[0]
        self.assertEqual(n, 0)

    def test_consistencia_status_e_duracao(self):
        invalidos = self.conn.execute("""SELECT COUNT(*) FROM vw_metricas_chamados
            WHERE (status='Aberto' AND resolucao_minutos IS NOT NULL)
               OR (status='Resolvido' AND resolucao_minutos IS NULL)
               OR resolucao_minutos < 0
        """).fetchone()[0]
        self.assertEqual(invalidos, 0)

    def test_consultas_executam(self):
        for arquivo, _, _ in QUESTOES:
            with self.subTest(arquivo=arquivo):
                colunas, linhas = consultar(self.conn, arquivo)
                self.assertTrue(colunas)
                self.assertTrue(linhas)

    def test_agregacao_mensal_fecha_total(self):
        _, linhas = consultar(self.conn, "04_tendencia_mensal.sql")
        self.assertEqual(sum(r[1] for r in linhas), self.resumo["chamados"])
        self.assertEqual([r[0] for r in linhas], ["2026-06", "2026-07", "2026-08", "2026-09"])

    def test_contagens_prioridades_fecham_total(self):
        _, linhas = consultar(self.conn, "02_perfil_de_prioridades.sql")
        self.assertEqual(sum(r[-1] for r in linhas), self.resumo["chamados"])

    def test_sla_somente_resolvidos(self):
        _, linhas = consultar(self.conn, "03_cumprimento_sla.sql")
        resolvidos = self.conn.execute("SELECT COUNT(*) FROM chamados WHERE status='Resolvido'").fetchone()[0]
        self.assertEqual(sum(r[1] for r in linhas), resolvidos)
        for linha in linhas:
            self.assertTrue(0 <= linha[2] <= linha[1])
            self.assertTrue(0 <= linha[3] <= 100)

    def test_consulta_parametrizada(self):
        filtro = "3 OR 1=1"
        encontrados = self.conn.execute(
            "SELECT COUNT(*) FROM chamados WHERE servico_id = ? AND status = ?",
            (filtro, "Aberto"),
        ).fetchone()[0]
        self.assertEqual(encontrados, 0)

    def test_plano_utiliza_indice_composto(self):
        _, linhas = consultar(self.conn, "10_plano_e_indices.sql")
        detalhes = " ".join(str(row[-1]) for row in linhas)
        self.assertIn("idx_chamados_servico_status", detalhes)


if __name__ == "__main__":
    unittest.main()
