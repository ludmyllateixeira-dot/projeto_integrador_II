# SITRIB — Sistema de Inteligência Tributária (Palmas/TO)

**Universidade Federal do Tocantins (UFT)**  
**Bacharelado Interdisciplinar em Inteligência Artificial (BIINAR)**  
**Eixo II — Projeto Integrador: Secretaria Municipal de Finanças (SEFIN Palmas)**  
**Período:** 2026/2  
**Coordenação:** Prof. Dr. David Nadler Prata  

---

## 👥 Identificação da Equipe e Papéis Ágeis

| Integrante | Matrícula | GitHub | Papel Ágil | Frente Técnica Principal |
| :--- | :---: | :---: | :---: | :--- |
| **Sofia Barros de Jesus** | 2026111954 | [`@24sofiabarros`](https://github.com/24sofiabarros) | **Scrum Master (SM)** | Orquestração do Pipeline ETL e Gestão do Repositório |
| **Ludmylla Teixeira** | 2026111980 | [`@ludmyllateixeira-dot`](https://github.com/ludmyllateixeira-dot) | **Product Owner (PO)** | Modelagem de Regras de Negócio e Arquitetura do Domínio |
| **Vitória Lopes** | 2026112100 | [`@vitiriaalopes123-source`](https://github.com/vitiriaalopes123-source) | **Desenvolvedora** | Análise Exploratória (EDA) e Painel MVP (Streamlit) |
| **Hyago Herrcolis Queiroz** | 2026112200 | [`@hyagoqueiroz-coder`](https://github.com/hyagoqueiroz-coder) | **Desenvolvedor** | Modelagem de Machine Learning e Motor de Scoring |
| **Maiara dos Santos** | 2026112300 | [`@maiarasantos-dev`](https://github.com/maiarasantos-dev) | **Desenvolvedora** | Governança de Dados, Auditoria LGPD e Testes de Qualidade |

---

## 🎯 Objetivo do Sistema

O **SITRIB** é uma plataforma de inteligência fiscal desenvolvida para otimizar e humanizar a gestão e cobrança da **Dívida Ativa Municipal de Palmas/TO**, cruzando dados fiscais de IPTU, ISSQN e taxas com indicadores socioeconômicos censitários do IBGE.

### Pilares Fundamentais:
1. **Justiça Fiscal e Proteção Social:** Diferenciação estrita entre a **insolvência por subsistência** (periferia / Jardins Aureny e Taquari — onde o IPTU Social e parcelamentos de até 10% da renda protegem o cidadão de execuções inviáveis) e a **inadimplência por estratégia de caixa** (Plano Diretor e Orla 14 Graciosa — onde mais de 75% da dívida ativa se concentra com liquidez comprovada).
2. **Eficiência Orçamentária:** Eliminação de execuções fiscais predatórias que custam mais aos cofres públicos (R$ 4.500 em média) do que o próprio débito executado.
3. **Machine Learning e Scoring:** Priorização dinâmica de cobrança com modelos preditivos calibrados por split temporal sem vazamento de dados.

---

## 🏗️ Arquitetura da Solução

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          FLUXO GERAL DO SITRIB                         │
└────────────────────────────────────────────────────────────────────────┘

  [ Portal NUCLEOGOV ]    [ API IBGE Palmas ]
  (180k+ Lançamentos)     (Setores Censitários)
          │                        │
          ▼                        ▼
 ┌──────────────────────────────────────────────────────────┐
 │  MÓDULO DE COLETA & PIPELINE ETL (src/coleta & src/etl)   │
 │  - Rate-limit ético (0.3s) e captura de cookies de sessão │
 │  - Camadas: data/bruto/ ➔ data/limpo/ ➔ data/pronto/     │
 │  - Expurgo de dados pessoais sensíveis (Anonimização)    │
 └────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
 ┌──────────────────────────────────────────────────────────┐
 │      INTELIGÊNCIA ARTIFICIAL & SCORING (models/ & src/)  │
 │  - Split temporal estrito (Treino até 2022 / Teste 2024) │
 │  - Modelos: Regressão Logística, Decision Tree,          │
 │             Random Forest (85,5%) e XGBoost (84,9%)      │
 │  - Scoring de Recuperabilidade (Alta, Média, Baixa)      │
 └────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
 ┌──────────────────────────────────────────────────────────┐
 │          PAINEL INTERATIVO MVP (Streamlit app.py)        │
 │  - Ranking de devedores por prioridade                   │
 │  - Mapa geoespacial de calor da inadimplência            │
 │  - Simulador de impacto de arrecadação potencial         │
 └──────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura de Diretórios

```text
projeto_integrador_II/
├── data/                        # Ciclo de vida dos dados (Medalhão)
│   ├── bruto/                   # Camada Bronze: JSONs datados da API
│   ├── limpo/                   # Camada Silver: Dados limpos e padronizados
│   └── pronto/                  # Camada Gold: Base pronta para IA
│
├── docs/                        # Documentação Técnica das Sprints
│   ├── requisitos_sprint1.md    # Sprint 1: Requisitos RF/RNF e MoSCoW
│   ├── resumo_entregas_sprint2.md # Sprint 2: Modelagem relacional e SQL
│   ├── manual_coleta_palmas.md  # Sprint 3: Manual oficial de coleta NUCLEOGOV
│   ├── relatorio_sprint3_pipeline_etl.md # Sprint 3: Relatório de ETL e camadas
│   ├── relatorio_eda_inadimplencia.md   # Sprint 3: Análise exploratória descritiva
│   ├── mapa_inadimplencia_palmas.html   # Sprint 3: Mapa geoespacial interativo
│   └── relatorio_sprint4_modelos_mvp.md # Sprint 4: Avaliação de IA e métricas
│
├── models/                      # Modelos serializados e scripts de treino
│   ├── decision_tree_baseline.joblib
│   ├── logistic_regression_baseline.joblib
│   ├── random_forest_debt_model.joblib  # Modelo campeão (F1: 91,67%)
│   ├── xgboost_debt_model.joblib
│   ├── model_metrics.json       # Métricas consolidadas
│   └── train_models.py          # Script de treinamento
│
├── notebooks/                   # Notebooks Jupyter da esteira de dados
│   ├── eda_inadimplencia.ipynb
│   └── sprint4_modelos_ia_scoring.ipynb
│
├── src/                         # Código-fonte modular da aplicação
│   ├── coleta/                  # Coletor HTTP do Portal Novo e API antiga
│   ├── etl/                     # Orquestrador de transformação e IBGE
│   ├── scoring/                 # Motor de regras de recuperabilidade
│   ├── pipeline/                # Pipeline de inferência em produção
│   └── models.py                # Entidades e dataclasses de domínio
│
├── tests/                       # Suíte de testes automatizados com Pytest
├── app.py                       # Interface web interativa em Streamlit (MVP)
├── requirements.txt             # Dependências Python isoladas
└── README.md                    # Visão geral da plataforma
```

---

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório e Criar Ambiente Virtual

```bash
git clone https://github.com/ludmyllateixeira-dot/projeto_integrador_II.git
cd projeto_integrador_II

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Pipeline ETL (Sprint 3)

```bash
# Executa a coleta, limpeza, enriquecimento e geração da base pronta
python src/etl/etl_sefin.py
```

### 4. Treinar os Modelos de Machine Learning (Sprint 4)

```bash
# Treina os baselines, Random Forest e XGBoost com split temporal
python models/train_models.py
```

### 5. Iniciar o Painel Interativo MVP (Streamlit)

```bash
streamlit run app.py
```
Acesse no seu navegador: `http://localhost:8501`.

### 6. Executar os Testes Automatizados

```bash
pytest
```

---

## 📚 Índice de Documentação Detalhada

* 📑 **Relatório Consolidado Geral (Sprints 1 a 4) [PDF Completo]:** [`docs/Relatorio_Consolidado_Sprints_1_a_4_SITRIB.pdf`](docs/Relatorio_Consolidado_Sprints_1_a_4_SITRIB.pdf)
* 📋 **Sprint 1 — Requisitos e Setup Ágil:** [`docs/requisitos_sprint1.md`](docs/requisitos_sprint1.md)
* 🗄️ **Sprint 2 — Banco Relacional e Arquitetura:** [`docs/resumo_entregas_sprint2.md`](docs/resumo_entregas_sprint2.md)
* 🌐 **Sprint 3 — Manual de Coleta NUCLEOGOV:** [`docs/manual_coleta_palmas.md`](docs/manual_coleta_palmas.md)
* ⚙️ **Sprint 3 — Relatório do Pipeline ETL:** [`docs/relatorio_sprint3_pipeline_etl.md`](docs/relatorio_sprint3_pipeline_etl.md)
* 📊 **Sprint 3 — Relatório de Análise Exploratória (EDA):** [`docs/relatorio_eda_inadimplencia.md`](docs/relatorio_eda_inadimplencia.md)
* 🗺️ **Sprint 3 — Mapa Geoespacial de Calor:** [`docs/mapa_inadimplencia_palmas.html`](docs/mapa_inadimplencia_palmas.html)
* 🤖 **Sprint 4 — Relatório de Modelos de IA e MVP:** [`docs/relatorio_sprint4_modelos_mvp.md`](docs/relatorio_sprint4_modelos_mvp.md)

---

*Projeto Integrador UFT — Ciência da Computação / BIINAR — Palmas/TO — 2026*
