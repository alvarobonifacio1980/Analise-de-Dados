-- Pergunta: qual equipe concentra o maior volume de chamados?
SELECT e.nome AS equipe,
       COUNT(c.chamado_id) AS total_chamados
FROM equipes AS e
LEFT JOIN servicos AS s ON s.equipe_id = e.equipe_id
LEFT JOIN chamados AS c ON c.servico_id = s.servico_id
GROUP BY e.equipe_id, e.nome
ORDER BY total_chamados DESC, equipe;
