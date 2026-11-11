-- Pergunta: o volume de chamados cresceu ou caiu em relação ao mês anterior?
WITH mensal AS (
    SELECT substr(aberto_em, 1, 7) AS mes,
           COUNT(*) AS total_chamados
    FROM chamados
    GROUP BY substr(aberto_em, 1, 7)
), tendencia AS (
    SELECT mes, total_chamados,
           LAG(total_chamados) OVER (ORDER BY mes) AS mes_anterior
    FROM mensal
)
SELECT mes, total_chamados, mes_anterior,
       CASE WHEN mes_anterior IS NOT NULL
            THEN ROUND(100.0 * (total_chamados - mes_anterior) / mes_anterior, 1)
       END AS variacao_percentual
FROM tendencia
ORDER BY mes;
