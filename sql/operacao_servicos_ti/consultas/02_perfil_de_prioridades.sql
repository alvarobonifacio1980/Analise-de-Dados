-- Pergunta: como as prioridades se distribuem entre os serviços?
SELECT s.nome AS servico,
       SUM(CASE WHEN c.prioridade = 'P1' THEN 1 ELSE 0 END) AS p1,
       SUM(CASE WHEN c.prioridade = 'P2' THEN 1 ELSE 0 END) AS p2,
       SUM(CASE WHEN c.prioridade = 'P3' THEN 1 ELSE 0 END) AS p3,
       SUM(CASE WHEN c.prioridade = 'P4' THEN 1 ELSE 0 END) AS p4,
       COUNT(c.chamado_id) AS total
FROM servicos AS s
LEFT JOIN chamados AS c ON c.servico_id = s.servico_id
GROUP BY s.servico_id, s.nome
ORDER BY total DESC, servico;
