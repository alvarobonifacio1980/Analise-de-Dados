-- Pergunta: como variam as avaliações entre chamados dentro e fora do SLA?
-- Associação descritiva: não implica causalidade.
SELECT CASE WHEN v.dentro_sla = 1 THEN 'Dentro do SLA' ELSE 'Fora do SLA' END AS situacao,
       COUNT(a.avaliacao_id) AS avaliacoes_recebidas,
       ROUND(AVG(a.nota), 2) AS nota_media,
       SUM(CASE WHEN a.nota >= 4 THEN 1 ELSE 0 END) AS notas_4_ou_5
FROM vw_metricas_chamados AS v
JOIN avaliacoes AS a ON a.chamado_id = v.chamado_id
WHERE v.status = 'Resolvido'
GROUP BY v.dentro_sla
ORDER BY v.dentro_sla DESC;
