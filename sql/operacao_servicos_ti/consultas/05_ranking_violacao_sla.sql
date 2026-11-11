-- Pergunta: onde estão concentrados os descumprimentos de SLA?
WITH indicadores AS (
    SELECT servico,
           COUNT(*) AS resolvidos,
           SUM(CASE WHEN dentro_sla = 0 THEN 1 ELSE 0 END) AS violacoes
    FROM vw_metricas_chamados
    WHERE status = 'Resolvido'
    GROUP BY servico
)
SELECT servico, resolvidos, violacoes,
       ROUND(100.0 * violacoes / resolvidos, 1) AS violacao_percentual,
       DENSE_RANK() OVER (ORDER BY violacoes DESC) AS posicao
FROM indicadores
ORDER BY posicao, servico;
