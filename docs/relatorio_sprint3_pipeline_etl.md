# UNIVERSIDADE FEDERAL DO TOCANTINS (UFT)
## Bacharelado Interdisciplinar em Inteligência Artificial (BIINAR)
### Eixo II — Projeto Integrador: Sistema de Inteligência Tributária (Sefin Palmas) | Período 2026/2

---

# Relatório Técnico de Entrega — Sprint 3 (Pipeline ETL)

| Campo | Detalhamento da Entrega |
| :--- | :--- |
| **Projeto** | Sistema de Inteligência Tributária — Priorização da cobrança da dívida ativa de Palmas-TO (Opção D) |
| **Sprint e Período** | Sprint 3 — Pipeline ETL (13/10/2026 a 27/10/2026) |
| **Módulo Âncora / Coordenação** | Módulo 5 — Coleta, Raspagem e Transformação Digital de Dados \| Prof. Dr. David Nadler Prata |
| **Equipe Executora** | Sofia Barros (SM), Ludmylla Teixeira (PO), Hyago Queiroz, Maiara dos Santos e Vitória Lopes (5 integrantes) |
| **Artefatos Entregues** | Coletor NUCLEOGOV em `src/coleta/`, Pipeline ETL em `src/etl/etl_sefin.py`, Relatório de EDA em `docs/`, Mapa Geoespacial e Base Padronizada |

---

## 1. Resumo Executivo

A Sprint 3 teve como objetivo fundamental **fazer o dado fluir de ponta a ponta sem intervenção manual**: desde a extração automatizada da API de Transparência da Prefeitura de Palmas (NUCLEOGOV) e dados abertos, passando pelo pipeline de limpeza, enriquecimento com indicadores socioeconômicos do IBGE e engenharia de atributos tributários, culminando na análise exploratória com mapa geoespacial e carga normalizada no banco de dados.

Todos os 4 entregáveis formais (E1 a E4) foram concluídos e validados:
- **E1 — Script de Coleta Automatizada:** Coletor HTTP robusto com controle de taxa (rate-limit >= 0.3s), captura de cookies e persistência em `data/bruto/`.
- **E2 — Pipeline ETL Funcional de Ponta a Ponta:** Script orquestrador [`src/etl/etl_sefin.py`](file:///C:/Users/morai/.gemini/antigravity/scratch/projeto_integrador_II/src/etl/etl_sefin.py) com transformação das camadas `bruto` ➔ `limpo` ➔ `pronto`.
- **E3 — Relatório de EDA e Mapa Geoespacial:** Documento analítico com frases de leitura ([`docs/relatorio_eda_inadimplencia.md`](file:///C:/Users/morai/.gemini/antigravity/scratch/projeto_integrador_II/docs/relatorio_eda_inadimplencia.md)) e mapa interativo Folium ([`docs/mapa_inadimplencia_palmas.html`](file:///C:/Users/morai/.gemini/antigravity/scratch/projeto_integrador_II/docs/mapa_inadimplencia_palmas.html)).
- **E4 — Reprodutibilidade:** Estrutura documentada no `README.md` com separação rigorosa de pastas e dependências.

---

## 2. Divisão de Trabalho da Equipe na Sprint 3

| Integrante | Papel no Time | Responsabilidade Técnica na Sprint 3 |
| :--- | :--- | :--- |
| **Sofia Barros de Jesus** | Scrum Master | Orquestração do pipeline ETL ponta a ponta (`src/etl/etl_sefin.py`), gestão das branches e alinhamentos semanais. |
| **Ludmylla Teixeira** | Product Owner | Modelagem conceitual das regras de negócio fiscais (IPTU Social), arquitetura de dados e homologação dos critérios de aceite. |
| **Vitória Lopes** | Desenvolvedora | Análise Exploratória de Dados (EDA), geração de gráficos de correlação/distribuição e elaboração do mapa geoespacial em Folium. |
| **Hyago Herrcolis Queiroz** | Desenvolvedor | Engenharia de atributos fiscais (cálculo de tempos de atraso, juros moratórios e sazonalidade) e estrutura das camadas de dados. |
| **Maiara dos Santos** | Desenvolvedora | Governança de dados, conformidade e anonimização estrita com a LGPD (zero PII) e validação dos logs de execução do pipeline. |

---

## 3. Arquitetura das Camadas de Dados

O ciclo de vida dos dados segue o padrão medalhão:
1. **Camada Bronze (`data/bruto/`):** Arquivos JSON e CSV crus extraídos da API do Portal Novo (`acessoainformacao.palmas.to.gov.br/api`) e da API do IBGE (Município 1721000 - Palmas), mantidos com carimbo de data/hora imutável.
2. **Camada Silver (`data/limpo/base_limpa.csv`):** Dados higienizados, tipos corrigidos, duplicidades eliminadas e regras de desagregação contábil aplicadas (eliminação de bitributação e armadilha 5.4).
3. **Camada Gold (`data/pronto/base_pronta.csv`):** Dados enriquecidos com renda média censitária, variáveis preditivas de negócio e identificadores pessoais 100% anonimizados.

---

## 4. Instruções de Execução

```bash
# 1. Executar o pipeline ETL completo
python src/etl/etl_sefin.py

# 2. Executar a suíte de testes de validação da coleta e transformações
pytest tests/test_coleta.py
```
