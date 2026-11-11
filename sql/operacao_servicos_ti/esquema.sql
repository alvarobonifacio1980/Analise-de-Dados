-- Dados 100% fictícios. Modelo didático, sem vínculo com bancos de terceiros.
-- Dialeto: SQLite 3.25+ (CTEs e funções de janela).
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS equipes (
    equipe_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS servicos (
    servico_id INTEGER PRIMARY KEY,
    equipe_id INTEGER NOT NULL,
    nome TEXT NOT NULL UNIQUE,
    criticidade TEXT NOT NULL CHECK (criticidade IN ('Alta', 'Média', 'Baixa')),
    FOREIGN KEY (equipe_id) REFERENCES equipes(equipe_id)
);

CREATE TABLE IF NOT EXISTS chamados (
    chamado_id INTEGER PRIMARY KEY,
    servico_id INTEGER NOT NULL,
    prioridade TEXT NOT NULL CHECK (prioridade IN ('P1', 'P2', 'P3', 'P4')),
    canal TEXT NOT NULL CHECK (canal IN ('Portal', 'E-mail', 'Telefone')),
    status TEXT NOT NULL CHECK (status IN ('Resolvido', 'Aberto')),
    aberto_em TEXT NOT NULL,     -- timestamp fictício sem fuso, formato AAAA-MM-DD HH:MM:SS
    encerrado_em TEXT,          -- NULL para chamados abertos
    FOREIGN KEY (servico_id) REFERENCES servicos(servico_id),
    CHECK (
        (status = 'Aberto' AND encerrado_em IS NULL)
        OR
        (status = 'Resolvido' AND encerrado_em IS NOT NULL AND encerrado_em >= aberto_em)
    )
);

CREATE TABLE IF NOT EXISTS avaliacoes (
    avaliacao_id INTEGER PRIMARY KEY,
    chamado_id INTEGER NOT NULL UNIQUE,
    nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
    FOREIGN KEY (chamado_id) REFERENCES chamados(chamado_id)
);

CREATE INDEX IF NOT EXISTS idx_chamados_abertura ON chamados(aberto_em);
CREATE INDEX IF NOT EXISTS idx_chamados_servico_status ON chamados(servico_id, status);
CREATE INDEX IF NOT EXISTS idx_chamados_prioridade ON chamados(prioridade);

-- Vista de consulta: metas hipotéticas por prioridade, duração e indicador SLA.
-- Metas são exemplos ilustrativos, não compromissos reais de serviços.
CREATE VIEW IF NOT EXISTS vw_metricas_chamados AS
WITH metas AS (
    SELECT c.chamado_id, c.servico_id, s.nome AS servico,
           s.equipe_id, e.nome AS equipe,
           c.prioridade, c.canal, c.status, c.aberto_em, c.encerrado_em,
           CASE c.prioridade
                WHEN 'P1' THEN 120
                WHEN 'P2' THEN 480
                WHEN 'P3' THEN 1440
                ELSE 2880
           END AS meta_minutos
    FROM chamados AS c
    JOIN servicos AS s ON s.servico_id = c.servico_id
    JOIN equipes AS e ON e.equipe_id = s.equipe_id
), tempos AS (
    SELECT metas.*,
           CASE WHEN encerrado_em IS NOT NULL
                THEN CAST((strftime('%s', encerrado_em) - strftime('%s', aberto_em)) / 60 AS INTEGER)
           END AS resolucao_minutos
    FROM metas
)
SELECT tempos.*,
       CASE WHEN resolucao_minutos IS NULL THEN NULL
            WHEN resolucao_minutos <= meta_minutos THEN 1
            ELSE 0
       END AS dentro_sla
FROM tempos;
