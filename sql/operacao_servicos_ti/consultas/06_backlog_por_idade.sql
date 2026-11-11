-- Pergunta: qual o envelhecimento do backlog na data de referência?
-- Data de corte fixa da simulação: 2026-10-01 00:00:00 (horário simulado, sem fuso).
WITH pendentes AS (
    SELECT equipe,
           CAST(julianday('2026-10-01 00:00:00') - julianday(aberto_em) AS INTEGER) AS dias_aberto
    FROM vw_metricas_chamados
    WHERE status = 'Aberto'
)
SELECT equipe,
       COUNT(*) AS total_abertos,
       SUM(CASE WHEN dias_aberto < 2 THEN 1 ELSE 0 END) AS ate_1_dia,
       SUM(CASE WHEN dias_aberto BETWEEN 2 AND 7 THEN 1 ELSE 0 END) AS de_2_a_7_dias,
       SUM(CASE WHEN dias_aberto > 7 THEN 1 ELSE 0 END) AS acima_7_dias
FROM pendentes
GROUP BY equipe
ORDER BY total_abertos DESC, equipe;
