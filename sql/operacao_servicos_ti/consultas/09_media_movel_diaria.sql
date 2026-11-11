-- Pergunta: qual a tendência recente do volume diário?
-- Gera um valor por dia observado, com janela móvel de até sete dias.
WITH diaria AS (
    SELECT substr(aberto_em, 1, 10) AS dia, COUNT(*) AS chamados
    FROM chamados
    GROUP BY substr(aberto_em, 1, 10)
)
SELECT dia, chamados,
       ROUND(AVG(chamados) OVER (ORDER BY dia
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS media_movel_7_dias
FROM diaria
ORDER BY dia;
