-- Pergunta: qual é o cumprimento das metas ilustrativas de atendimento?
-- Apenas chamados resolvidos entram no denominador de SLA.
WITH resolvidos AS (
    SELECT servico, equipe, dentro_sla, resolucao_minutos
    FROM vw_metricas_chamados
    WHERE status = 'Resolvido'
)
SELECT servico,
       COUNT(*) AS total_resolvidos,
       SUM(dentro_sla) AS dentro_da_meta,
       ROUND(100.0 * AVG(dentro_sla), 1) AS sla_percentual,
       ROUND(AVG(resolucao_minutos), 1) AS tempo_medio_minutos
FROM resolvidos
GROUP BY servico
ORDER BY sla_percentual ASC, total_resolvidos DESC;
