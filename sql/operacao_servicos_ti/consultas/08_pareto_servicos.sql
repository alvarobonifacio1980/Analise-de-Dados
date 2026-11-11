-- Pergunta: quais serviços acumulam 80% ou mais do volume de chamados?
WITH totais AS (
    SELECT s.nome AS servico, COUNT(c.chamado_id) AS quantidade
    FROM servicos AS s
    LEFT JOIN chamados AS c ON c.servico_id = s.servico_id
    GROUP BY s.servico_id, s.nome
), participacoes AS (
    SELECT servico, quantidade,
           ROUND(100.0 * quantidade / SUM(quantidade) OVER (), 1) AS percentual,
           ROUND(100.0 * SUM(quantidade) OVER (ORDER BY quantidade DESC, servico
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) /
               SUM(quantidade) OVER (), 1) AS acumulado_percentual
    FROM totais
)
SELECT servico, quantidade, percentual, acumulado_percentual
FROM participacoes
ORDER BY quantidade DESC, servico;
