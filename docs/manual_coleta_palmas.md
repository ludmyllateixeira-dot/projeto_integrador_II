# Manual de Coleta de Dados da Prefeitura de Palmas

**Guia prático para a Sprint 3 — Coleta e ETL (Módulo 5) do Projeto Integrador do Eixo II.**  
*Universidade Federal do Tocantins (UFT) — BIINAR*  
*Coordenação: Prof. Dr. David Nadler Prata*

---

## Sumário
1. [Panorama: Existem Duas APIs](#1-panorama-existem-duas-apis)
2. [Regras de Conduta e Ética de Coleta](#2-regras-de-conduta-e-ética-de-coleta)
3. [Portal Novo (NUCLEOGOV) — Operação Oficial](#3-portal-novo-nucleogov--operação-oficial)
4. [API Antiga — Série Histórica](#4-api-antiga--série-histórica)
5. [As Cinco Armadilhas de Coleta](#5-as-cinco-armadilhas-de-coleta)
6. [Robustez e Estratégias de Download](#6-robustez-e-estratégias-de-download)
7. [Checklist de Qualidade e Entrega](#7-checklist-de-qualidade-e-entrega)

---

## 1. Panorama: Existem Duas APIs

A Prefeitura de Palmas publica dados por dois sistemas distintos, com protocolos e esquemas não intercambiáveis:

| Característica | Portal Novo (NUCLEOGOV) | API Antiga |
| :--- | :--- | :--- |
| **Endereço Base** | `acessoainformacao.palmas.to.gov.br/api` | `integracao.palmas.to.gov.br/apirest/` |
| **Protocolo** | HTTPS válido | HTTP (o HTTPS possui certificado quebrado) |
| **Método HTTP** | `POST` com formulário urlencoded | `GET` com parâmetros de consulta na URL |
| **Período Temporal** | Atualizado em tempo real (mês corrente) | Série histórica congelada em junho de 2021 |
| **Conteúdo Principal** | Receitas, despesas, servidores, contratos e licitações | Gastos diretos, arrecadação pontual e folha (489k) |
| **Documentação Oficial** | Não documentado publicamente | `portaldatransparencia.palmas.to.gov.br/webservice/` |

> **Atenção:** Os dois sistemas não compartilham identificadores nem esquema. Unificá-los sem uma chave de ligação explícita gera inconsistência analítica.

---

## 2. Regras de Conduta e Ética de Coleta

Conforme exigido pelo plano de ensino do BIINAR (Seção 11 - Rigor Ético):
1. **Pausa entre requisições (Rate-Limit):** Utilizar no mínimo **0,3 segundos** de delay (`time.sleep(0.3)`). Requisições em laço fechado sobrecarregam o servidor público municipal.
2. **Sem automação recorrente desnecessária:** Baixe os lotes, armazene em `data/bruto/` com carimbo de data/hora e processe sobre os arquivos persistidos.
3. **Data e rastreabilidade:** Sempre documentar a data da extração no nome do arquivo (ex.: `dados_sefin_YYYYMMDD_HHMM.json`).
4. **Proteção de Dados Pessoais (LGPD):** A API pública não expõe identificadores fiscais individuais completos; nunca busque contornos para desanonimizar cidadãos.
5. **Timeouts explícitos:** Todas as chamadas de rede devem conter `timeout=60` ou `timeout=90`.

---

## 3. Portal Novo (NUCLEOGOV) — Operação Oficial

### 3.1 Funcionamento do Endpoint
O endpoint recebe requisições `POST` em formato `application/x-www-form-urlencoded` com os seguintes parâmetros:
* `multi_request`: sempre `"true"`
* `params`: JSON serializado contendo o dicionário com chave `"k1"`:
  * `acao`: operação alvo (ex.: `"sgreceitas/listar"`)
  * `limit`: paginação por offset no formato `"offset, quantidade"` (ex.: `"0, 1000"`)
  * `order`: `{}` para ordenação padrão

### 3.2 Módulos Disponíveis e Endpoints

| Módulo | Ação (`acao`) | Registros Médios | Referer Obrigatório |
| :--- | :--- | :---: | :--- |
| **Receitas** | `sgreceitas/listar` | ~180.976 | `/cidadao/transparencia/sgreceitas` |
| **Contratos** | `sgcontratos/listar` | ~8.897 | `/cidadao/transparencia/sgcontratos` |
| **Despesas** | `sgdespesas/listar` | ~3.412 | `/cidadao/transparencia/sgdespesas` |
| **Licitações** | `sglicitacoes/listar` | ~2.161 | `/cidadao/transparencia/sglicitacoes` |
| **Servidores** | `sgservidores/listar` | ~16.116 | `/cidadao/transparencia/sgservidores` |

### 3.3 Cabeçalhos HTTP Mandatórios
```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://acessoainformacao.palmas.to.gov.br/cidadao/transparencia/sgreceitas",
    "Origin": "https://acessoainformacao.palmas.to.gov.br"
}
```

---

## 4. As Cinco Armadilhas de Coleta

1. **Armadilha 5.1 — User-Agent Ausente:** O servidor bloqueia clientes com identificador padrão (como `python-requests`), retornando HTTP 403 ou página vazia.
2. **Armadilha 5.2 — Cookies de Sessão:** É necessário realizar um `GET` prévio na página de referência do módulo para carregar cookies de sessão válidos antes de disparar o `POST`.
3. **Armadilha 5.3 — Tamanho de Página Excessivo:** Páginas com mais de 1.000 registros sofrem *timeout*. Utilize sempre `limit="offset, 1000"`.
4. **Armadilha 5.4 — Dupla Contagem Orçamentária:** A contabilidade municipal agrega lançamentos analíticos e sintéticos no mesmo feed; a limpeza da camada Silver deve filtrar níveis hierárquicos para não inflar a arrecadação.
5. **Armadilha 5.5 — Volatilidade de Fechamento Contábil:** Números de arrecadação do mês corrente podem sofrer estornos ou retificações da Sefin; registre a data exata da extração.

---

## 5. Implementação de Referência no SITRIB

A classe oficial de coleta do projeto está implementada e documentada em:
* [`src/coleta/coleta_api.py`](file:///C:/Users/morai/.gemini/antigravity/scratch/projeto_integrador_II/src/coleta/coleta_api.py)
* Orquestrador de ETL: [`src/etl/etl_sefin.py`](file:///C:/Users/morai/.gemini/antigravity/scratch/projeto_integrador_II/src/etl/etl_sefin.py)
