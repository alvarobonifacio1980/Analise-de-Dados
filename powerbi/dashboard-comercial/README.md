# Dashboard Comercial — Power BI

**Status:** case descritivo publicado; dashboards originais preservados, sem previsão de retrabalho nesta fase. Este é o nome oficial do projeto no repositório.

## Objetivo

Explorar indicadores de desempenho comercial e apoiar decisões sobre evolução de receitas, mix de produtos e marcas, distribuição geográfica e perfil de clientes. Projeto desenvolvido como exercício prático em Power BI; a origem dos dados, as transformações e os cálculos ainda precisam ser documentados e auditados antes de uma apresentação pública definitiva.

## Painéis observados

A análise visual foi realizada a partir de três capturas fornecidas pelo autor, além do arquivo original do Power BI.

### Visão executiva

- Indicadores exibidos na captura: **Receita R$ 548,51 milhões**, **Produtos vendidos 2,12 milhões**, **Ticket médio R$ 478,65**, **Clientes 18,48 mil**. São valores da tela apresentada, não métricas auditadas.
- Evolução mensal do faturamento entre 2022 e 2024, com aparente mudança de patamar no início de 2023.
- Distribuição de quantidades por gênero; mapa de faturamento por continente; ranking de faturamento por marca.

### Explorações adicionais

- Tabela com quantidades vendidas por país e total exibido de **2.117.268 unidades**.
- Quantidade vendida por faixa etária (Adulto, Jovem e Sênior).
- Matriz de faturamento cruzando categoria e faixa etária.

## Estrutura confirmada no arquivo

O relatório contém **4 páginas e 19 visuais**. A página inicial reúne quatro indicadores em cartões e visualizações de receita ao longo do tempo, vendas por gênero, faturamento por marca e continente. Outras páginas trazem quantidade por país e faixa etária, indicadores de devolução/vendas on-line e matriz de faturamento por categoria e faixa etária.

Nos visuais do PBIX foram identificadas **medidas nomeadas**: `Fat total`, `Total de Vendas`, `ticket medio`, `Qtde_clientes`, `Total Devoluções`, `% devoluções` e `Vendas on line`. Também estão referenciadas as tabelas `Base Vendas`, `Cadastro de clientes`, `Cadastro de produtos` e `Cadastro de lojas`. Isso demonstra uso das medidas nos gráficos, mas **não valida as expressões DAX nem os relacionamentos**.

## Competências que o case pode demonstrar

- Estruturação de indicadores executivos e visualizações de negócio.
- Análise temporal, geográfica, de produtos, marcas e segmentação de clientes.
- Uso de gráficos de linha/área, barras, rosca, mapa, cartões e matriz/tabela.
- Interação e contextualização gerencial — **ainda depende de inspeção do relatório no Power BI Desktop**.

> A presença das visualizações **não comprova por si só** qualidade de medidas DAX, modelagem, Power Query ou atualização dos dados. Essas competências só serão destacadas como demonstradas após revisão técnica.

## Revisão de qualidade — pontos observados

1. **Consistência dos indicadores:** conferir definição e denominador de «ticket médio». Não presumir que receita dividida por produtos ou clientes seja seu cálculo. Conferir também se «Total de Vendas por Gênero» representa quantidade de produtos vendidos, transações ou outro indicador.
2. **Quebra de patamar em jan/2023:** revisar mudança acentuada de faturamento, datas, cobertura e eventuais alterações de origem/ETL antes de formular conclusões.
3. **Unidade monetária:** uniformizar o padrão entre «R$» nos cartões e «$» na matriz de categorias.
4. **Hierarquia e espaço:** reduzir a altura do título e equilibrar tamanho dos cartões para ampliar a área destinada às análises.
5. **Legibilidade:** rever o contraste do título do mapa e o excesso de sombra nos cards; padronizar cores para que tenham significado consistente.
6. **Rolagem e recortes:** rever o ranking por marca, a tabela por país e a matriz categoria × faixa etária, que aparecem parcialmente cortados nas capturas.
7. **Confiabilidade:** auditar dados, relacionamento entre tabelas, Power Query e medidas DAX no arquivo original.
8. **Publicação:** conferir se dados e eventuais recursos de treinamento têm autorização para distribuição. Exportar capturas apenas depois da revisão.

## Candidaturas e portfólio

Este projeto é candidato prioritário para demonstrar conhecimento aplicado em **Power BI, indicadores comerciais, visualização e análise de dados**, em conjunto com os demais cases do repositório. Para uma versão profissional, a apresentação deve explicar: pergunta de negócio, fonte de dados, preparação e modelagem, indicadores/DAX, principais descobertas e limitações.

**Escopo atual:** documentação do trabalho existente para evidenciar familiaridade prática com Power BI. Ajustes visuais, auditoria DAX e distribuição do PBIX ficam fora da prioridade atual. O foco principal do portfólio continua em Python, dados e IA.
