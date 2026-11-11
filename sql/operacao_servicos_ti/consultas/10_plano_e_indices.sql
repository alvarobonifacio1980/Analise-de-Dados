-- Pergunta: como avaliar se os índices atendem uma consulta frequente?
-- EXPLAIN QUERY PLAN mostra a estratégia usada pelo SQLite (pode mudar por versão).
EXPLAIN QUERY PLAN
SELECT c.chamado_id, c.status, c.aberto_em
FROM chamados AS c
WHERE c.servico_id = 3
  AND c.status = 'Aberto'
ORDER BY c.aberto_em DESC
LIMIT 20;
