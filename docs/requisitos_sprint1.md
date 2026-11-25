# Documentação de Requisitos e Setup Ágil — Sprint 1

**Universidade Federal do Tocantins (UFT) — BIINAR**  
**Eixo II — Projeto Integrador: Sistema de Inteligência Tributária (Sefin Palmas)**  
**Período:** 2026/2

---

## 1. Identificação da Equipe e Papéis Ágeis

| Integrante | Matrícula | Usuário GitHub (@) | Papel Principal no Time |
| :--- | :--- | :--- | :--- |
| **Sofia Barros de Jesus** | 2026111954 | `@24sofiabarros` | **Scrum Master (SM)** |
| **Ludmylla Teixeira** | 2026111980 | `@ludmyllateixeira-dot` | **Product Owner (PO)** |
| **Vitória Lopes** | 2026112100 | `@vitiriaalopes123-source` | **Desenvolvedora (EDA / Frontend)** |
| **Hyago Herrcolis Queiroz** | 2026112200 | `@hyagoqueiroz-coder` | **Desenvolvedor (ML / Scoring)** |
| **Maiara dos Santos** | 2026112300 | `@maiarasantos-dev` | **Desenvolvedora (Governança / LGPD)** |

---

## 2. Fundamentação e Dinâmica dos Papéis Ágeis

### A) Product Owner (PO) — Ludmylla Teixeira
* **Atribuições:** Responsável máxima pela visão do produto, gestão e priorização do Backlog do Produto, interlocução com os requisitos fazendários (Sefin Palmas / regras de IPTU Social) e validação dos critérios de aceite das entregas.
* **Critérios de Validação:** A PO valida os incrementos por meio de testes funcionais, conferência de memória de cálculo e checagem de conformidade com as diretrizes do plano de ensino do BIINAR.

### B) Scrum Master (SM) — Sofia Barros de Jesus
* **Atribuições:** Facilitadora do método ágil Scrum na equipe, remoção ativa de impedimentos técnicos e operacionais, moderação das cerimônias semanais (Dailies/Semanais, Sprint Planning, Review e Retrospectiva) e controle de versão das branches no GitHub.
* **Comunicação:** Reuniões de alinhamento com registro em diário de bordo e canal oficial de comunicação assíncrona.

---

## 3. Especificação de Requisitos Funcionais (RF)

| ID | Nome do Requisito | Descrição / História de Usuário | Critérios de Aceite (Testáveis) |
| :--- | :--- | :--- | :--- |
| **RF01** | Cadastro de Contribuintes | Registro de pessoas físicas e jurídicas no sistema fazendário. | 1. Validação de formato de CPF/CNPJ.<br>2. Bloqueio de duplicidades no cadastro. |
| **RF02** | Registro de Dívida Ativa | Cadastro de débitos tributários de IPTU, ISSQN e taxas. | 1. Associação obrigatória a um contribuinte.<br>2. Armazenamento de valor original, ano de exercício e data de vencimento. |
| **RF03** | Proteção ao IPTU Social | Aplicação de regras de imunidade/isenção para famílias de baixa renda. | 1. Verificação de flag `possui_iptu_social`.<br>2. Bloqueio de ajuizamento contra imóveis cadastrados no benefício social. |
| **RF04** | Cálculo de Juros e Multas | Aplicação de encargos moratórios conforme a legislação municipal de Palmas. | 1. Atualização com base no IPCA e teto de juros moratórios.<br>2. Memória de cálculo transparente. |
| **RF05** | Consulta Cadastral Unificada | Busca de informações por documento fiscal (CPF/CNPJ). | 1. Retorno em tempo hábil de débitos e imóveis vinculados.<br>2. Mensagem amigável para chave inexistente. |
| **RF06** | Fila de Priorização de Cobrança | Ordenação de devedores com base em pontuação e capacidade financeira. | 1. Listagem decrescente por score de prioridade.<br>2. Discriminação por faixas de recuperação. |
| **RF07** | Simulação de Parcelamento | Projeção de acordos fiscais com opções de parcelas e descontos. | 1. Simulação sem alterar dados definitivos no banco.<br>2. Limitação das parcelas à capacidade socioeconômica. |
| **RF08** | Ingestão Automatizada de Dados | Carga de lançamentos da prefeitura e dados abertos. | 1. Tratamento de rate-limit e paginação.<br>2. Preservação dos dados brutos com timestamp. |
| **RF09** | Predição de Inadimplência | Inferência preditiva da probabilidade de inadimplemento por IA. | 1. Modelo treinado com split temporal sem data leakage.<br>2. Registro de métricas (acurácia, precisão, recall, F1). |
| **RF10** | Painel Analítico Interativo | Interface para apoio à tomada de decisão do auditor fiscal. | 1. Visualização de rankings, métricas e mapa de calor territorial.<br>2. Exportação de relatórios executivos. |

---

## 4. Requisitos Não Funcionais (RNF)

| ID | Categoria | Descrição da Restrição | Métrica / Forma de Teste |
| :--- | :--- | :--- | :--- |
| **RNF01** | Tecnologia / Backend | O sistema deve ser desenvolvido em Python 3.12+ utilizando o padrão arquitetural MVC. | Verificação de sintaxe e execução no interpretador oficial. |
| **RNF02** | Portabilidade | As dependências de pacotes devem estar isoladas e descritas em manifesto. | Instalação reprodutível com `pip install -r requirements.txt`. |
| **RNF03** | Usabilidade | O sistema e painéis devem fornecer respostas imediatas e claras em todas as operações. | Feedback visual/textual de sucesso ou erro com tempo de resposta < 2s. |
| **RNF04** | Conformidade LGPD | Não expor dados pessoais identificáveis (PII) em relatórios analíticos ou modelos de IA. | Anonimização/mascaramento de CPF, e-mail e telefone antes do armazenamento e treinamento. |
| **RNF05** | Segurança & Integridade | Garantir atomicidade nas operações de carga relacional do banco de dados. | Transações SQL com *rollback* em caso de falha de integridade. |

---

## 5. Matriz de Priorização MoSCoW

* **Must Have (Essencial para o MVP):** RF01, RF02, RF03, RF04, RF08, RF09, RNF01, RNF02, RNF04.
* **Should Have (Alta prioridade):** RF05, RF06, RF07, RF10, RNF03, RNF05.
* **Could Have (Desejável):** Geração de relatórios em múltiplos formatos (PDF/Excel), temas de alto contraste.
* **Won't Have (Fora do escopo da entrega inicial):** Integração bancária direta para emissão de boletos PIX automáticos.
