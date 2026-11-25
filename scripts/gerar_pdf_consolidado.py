import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Capa limpa sem cabeçalho/rodapé
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Cabeçalho
        self.drawString(54, 800, "SITRIB-Palmas • Relatório Técnico Consolidado (Sprints 1 a 4)")
        self.drawRightString(541, 800, "UFT / BIINAR • SEFIN Palmas-TO")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792)
        
        # Rodapé
        self.line(54, 45, 541, 45)
        self.drawString(54, 32, "Projeto Integrador II • Inteligência Tributária e Governança Fazendária")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(541, 32, page_str)
        self.restoreState()


def build_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Estilos customizados
    primary_color = colors.HexColor("#0f172a")    # Azul ardósia profundo
    accent_blue = colors.HexColor("#1e40af")      # Azul corporativo
    teal_color = colors.HexColor("#0284c7")       # Azul claro fazendário
    dark_neutral = colors.HexColor("#334155")
    light_bg = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#e2e8f0")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        alignment=0
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=accent_blue,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=dark_neutral,
        spaceAfter=6,
        alignment=4 # Justificado
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0369a1")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=primary_color
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # =========================================================================
    # 1. CAPA / CABEÇALHO DO DOCUMENTO
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("UNIVERSIDADE FEDERAL DO TOCANTINS (UFT)", ParagraphStyle('Uni', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor("#64748b"))))
    story.append(Paragraph("CURSO DE INTELIGÊNCIA ARTIFICIAL E CIÊNCIA DE DADOS • PROJETO INTEGRADOR II (BIINAR)", ParagraphStyle('SubUni', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor("#94a3b8"))))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=3, color=accent_blue, spaceBefore=0, spaceAfter=15))

    story.append(Paragraph("SITRIB-Palmas: Sistema Inteligente de Recuperação Tributária", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Relatório Técnico Consolidado de Engenharia de Dados, Governança e Inteligência Artificial (Sprints 1, 2, 3 e 4)", subtitle_style))
    story.append(Spacer(1, 15))

    # Tabela com Metadados do Projeto e Equipe
    equipe_data = [
        [Paragraph("<b>Projeto:</b>", table_cell_bold), Paragraph("SITRIB — Sistema de Inteligência Tributária (Palmas-TO)", table_cell_style)],
        [Paragraph("<b>Órgão Parceiro:</b>", table_cell_bold), Paragraph("Secretaria Municipal de Finanças de Palmas (SEFIN Palmas)", table_cell_style)],
        [Paragraph("<b>Orientador / Coordenação:</b>", table_cell_bold), Paragraph("Prof. Dr. David Nadler Prata (UFT / BIINAR)", table_cell_style)],
        [Paragraph("<b>Repositório Oficial:</b>", table_cell_bold), Paragraph("github.com/ludmyllateixeira-dot/projeto_integrador_II", table_cell_style)],
        [Paragraph("<b>Data da Consolidação:</b>", table_cell_bold), Paragraph("Novembro de 2026 • Versão 2.0 Operacional", table_cell_style)],
    ]
    t_meta = Table(equipe_data, colWidths=[130, 357])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    # Tabela da Equipe Executora
    story.append(Paragraph("Quadro de Divisão Oficial de Papéis da Equipe", h2_style))
    equipe_roles = [
        [Paragraph("Membro", table_header_style), Paragraph("Papel Oficial", table_header_style), Paragraph("Principais Responsabilidades Técnicas", table_header_style)],
        [Paragraph("<b>Sofia Barros de Jesus</b>", table_cell_style), Paragraph("Scrum Master & Eng. Dados", table_cell_style), Paragraph("Arquitetura de dados 3FN, pipeline ETL, orquestração e conciliação bancária.", table_cell_style)],
        [Paragraph("<b>Ludmylla Teixeira</b>", table_cell_style), Paragraph("Product Owner & Negócio", table_cell_style), Paragraph("Visão de produto, requisitos fazendários, homologação e conformidade.", table_cell_style)],
        [Paragraph("<b>Vitória Lopes</b>", table_cell_style), Paragraph("Frontend & Analista EDA", table_cell_style), Paragraph("Interface web interativa em Streamlit, análise exploratória e mapas de calor.", table_cell_style)],
        [Paragraph("<b>Hyago Herrcolis Queiroz</b>", table_cell_style), Paragraph("Cientista de Dados (ML)", table_cell_style), Paragraph("Engenharia de features, treinamento supervisionado e motor de scoring (0 a 100).", table_cell_style)],
        [Paragraph("<b>Maiara dos Santos</b>", table_cell_style), Paragraph("Governança & LGPD", table_cell_style), Paragraph("Mascaramento de dados fiscais, auditoria algorítmica e validação de pipeline.", table_cell_style)]
    ]
    t_equipe = Table(equipe_roles, colWidths=[120, 110, 257])
    t_equipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent_blue),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_equipe)

    story.append(Spacer(1, 15))
    story.append(Paragraph("Sumário Executivo e Propósito deste Documento", h2_style))
    story.append(Paragraph(
        "Este documento foi elaborado para fundamentar tecnicamente a banca de avaliação acadêmica e a apresentação do trabalho final, "
        "reunindo em uma narrativa coesa e auditável todas as quatro etapas de desenvolvimento do SITRIB. Ele detalha a motivação fiscal "
        "do Município de Palmas, as escolhas de arquitetura de dados (banco relacional, estruturas em memória e pipeline ETL medalhão), "
        "a estratégia de modelagem preditiva com aprendizado de máquina supervisionado e o funcionamento operacional do painel web MVP.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # 2. ESCLARECIMENTO FUNDAMENTAL: O PANORAMA DAS DUAS APIS DE PALMAS
    # =========================================================================
    story.append(Paragraph("1. Panorama Crítico: A Origem dos Dados e as Duas APIs de Palmas", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "Um dos aspectos técnicos mais importantes do projeto — e ponto indispensável para a apresentação — é a compreensão precisa "
        "sobre os sistemas fazendários do Município de Palmas. A Prefeitura publica dados fiscais por meio de <b>dois sistemas independentes</b>, "
        "que não se comunicam e possuem esquemas e finalidades complementares:",
        body_style
    ))

    apis_data = [
        [Paragraph("Critério", table_header_style), Paragraph("Portal Novo (NUCLEOGOV)", table_header_style), Paragraph("API Antiga (Histórica SEFIN)", table_header_style)],
        [Paragraph("<b>Endereço Base</b>", table_cell_style), Paragraph("acessoainformacao.palmas.to.gov.br/api", table_cell_style), Paragraph("integracao.palmas.to.gov.br/apirest/", table_cell_style)],
        [Paragraph("<b>Protocolo / Método</b>", table_cell_style), Paragraph("HTTPS v2 • POST urlencoded com JSON params", table_cell_style), Paragraph("HTTP padrão • GET com parâmetros na URL", table_cell_style)],
        [Paragraph("<b>Horizonte Temporal</b>", table_cell_style), Paragraph("Tempo real / mês corrente atualizado", table_cell_style), Paragraph("Série temporal histórica consolidada até jun/2021", table_cell_style)],
        [Paragraph("<b>Conteúdo Principal</b>", table_cell_style), Paragraph("Receitas orçamentárias gerais, contratos, licitações", table_cell_style), Paragraph("Registros operacionais detalhados, arrecadação, passivo", table_cell_style)],
        [Paragraph("<b>Papel no SITRIB</b>", table_cell_style), Paragraph("Alvo do módulo coletor contínuo (Sprint 3 - E1)", table_cell_style), Paragraph("<b>Base de calibração e treino da IA (2.499 devedores)</b>", table_cell_bold)],
    ]
    t_apis = Table(apis_data, colWidths=[100, 190, 197])
    t_apis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_apis)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Por que utilizamos a API Antiga para a Base de Dívida Ativa e Machine Learning?", h2_style))
    story.append(Paragraph(
        "A API do portal novo (NUCLEOGOV) expõe dados orçamentários consolidados da administração pública, mas <b>não disponibiliza os registros "
        "individualizados de devedores por CPF/CNPJ</b>, em estrito respeito ao Sigilo Fiscal (Art. 198 do Código Tributário Nacional) e à LGPD. "
        "Para possibilitar a modelagem preditiva de inadimplência, a equipe utilizou o histórico consolidado da <b>API antiga</b> como base primária, "
        "composta por 2.499 registros tributários reais de Palmas.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Governança e Mascaramento LGPD:</b> Conforme supervisionado por Maiara dos Santos, nenhum dado pessoal real dos cidadãos foi exposto. "
        "Os CPFs e nomes foram submetidos a um algoritmo determinístico de anonimização e mascaramento cadastral (exibindo apenas o prefixo e sufixo "
        "com caracteres de proteção como <code>***.123.456-**</code>). Todas as grandezas financeiras reais (valores de IPTU, ISSQN, ITBI, juros, "
        "multas, tempo em atraso e setor geográfico do município) foram preservadas com 100% de integridade analítica para treino dos algoritmos.",
        body_style
    ))

    # =========================================================================
    # 3. SPRINT 1: REQUISITOS, ESCOPO E RIGOR ÉTICO
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Sprint 1: Concepção, Requisitos de Negócio e Governança Ética", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "A Sprint 1 estabeleceu os alicerces teóricos e estratégicos do SITRIB sob a liderança de Ludmylla Teixeira (Product Owner), "
        "definindo como a ciência de dados pode mitigar a histórica ineficiência do estoque de dívida ativa municipal sem penalizar famílias em vulnerabilidade social.",
        body_style
    ))
    story.append(Paragraph("Principais Entregas da Sprint 1:", h2_style))
    story.append(Paragraph("• <b>Mapeamento do Problema Fazendário:</b> A cobrança tributária convencional adota critérios puramente cronológicos ou por valor facial, ajuizando execuções fiscais de alto custo processual para devedores sem capacidade financeira e deixando prescrever débitos de contribuintes com alta solvência.", bullet_style))
    story.append(Paragraph("• <b>Requisitos Funcionais (RFs):</b> Classificação automática de recuperabilidade de 0 a 100, visualização geoespacial da inadimplência, filtros por espécie tributária e canal de cobrança recomendado.", bullet_style))
    story.append(Paragraph("• <b>Requisitos Não-Funcionais (RNFs):</b> Latência de inferência menor que 200ms para listas de até 10.000 contribuintes, conformidade estrita com a LGPD (Lei 13.709/2018) e segurança jurídica com base na Lei de Responsabilidade Fiscal.", bullet_style))
    story.append(Paragraph("• <b>Princípio Ético da Função Social do Tributo:</b> Exclusão automática de munícipes enquadrados no programa IPTU Social de qualquer ação coercitiva ou ajuizamento, canalizando a estes apenas orientações de anistia e remissão legal.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 4. SPRINT 2: INFRAESTRUTURA RELACIONAL (3FN) E ALGORITMOS
    # =========================================================================
    story.append(Paragraph("3. Sprint 2: Infraestrutura Relacional (3FN) e Estruturas de Dados Avançadas", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "A Sprint 2 traduziu os requisitos conceituais em implementações concretas de engenharia de software e persistência de dados. "
        "Foram desenvolvidos os esquemas físicos de banco de dados e algoritmos de alto desempenho em memória para suportar análises em tempo real.",
        body_style
    ))

    story.append(Paragraph("3.1 Modelagem Relacional Normalizada (3ª Forma Normal - 3FN)", h2_style))
    story.append(Paragraph(
        "A estrutura do banco de dados (armazenada em <code>src/banco/schema_3fn.sql</code>) eliminou todas as dependências funcionais parciais "
        "e transitivas, garantindo integridade referencial com chaves estrangeiras restritivas:",
        body_style
    ))
    story.append(Paragraph("• <b>Tabela <code>contribuinte</code>:</b> Chave substituta <code>id_contribuinte</code>, campo <code>cpf_cnpj_mascarado</code> com restrição de unicidade, classificação de porte empresarial e flag booleana <code>isencao_iptu_social</code>.", bullet_style))
    story.append(Paragraph("• <b>Tabela <code>imovel</code>:</b> Identificador cadastral <code>inscricao_imobiliaria</code>, chave estrangeira para o contribuinte responsável com integridade <code>ON UPDATE CASCADE ON DELETE RESTRICT</code>, setor fiscal e valor venal.", bullet_style))
    story.append(Paragraph("• <b>Tabela <code>divida_ativa</code>:</b> Código CDA, vínculo com o imóvel, restrições de domínio <code>CHECK</code> para as espécies tributárias (IPTU, ISS, ITBI, TAXAS), status de cobrança e campo numérico <code>score_recuperabilidade</code>.", bullet_style))

    story.append(Spacer(1, 5))
    story.append(Paragraph("3.2 Estruturas de Dados Avançadas em Memória e Complexidade Big-O", h2_style))
    story.append(Paragraph(
        "Para permitir operações analíticas ultra-rápidas no servidor antes da gravação em disco, foram codificadas estruturas especializadas em Python puro (<code>src/estruturas/arquitetura_dados.py</code>):",
        body_style
    ))

    estruturas_data = [
        [Paragraph("Estrutura Implementada", table_header_style), Paragraph("Algoritmo / Mecânica", table_header_style), Paragraph("Complexidade Big-O", table_header_style), Paragraph("Aplicação no Sistema SITRIB", table_header_style)],
        [Paragraph("<b>Grafo de Relações Tributárias</b>", table_cell_style), Paragraph("Busca em Largura (BFS) em lista de adjacências", table_cell_style), Paragraph("<b>O(V + E)</b>", table_cell_bold), Paragraph("Identifica confusão patrimonial, sócios ocultos e rede de imóveis do mesmo devedor.", table_cell_style)],
        [Paragraph("<b>Fila de Prioridade Fiscal (Heap)</b>", table_cell_style), Paragraph("Heap Máximo binário via módulo <code>heapq</code>", table_cell_style), Paragraph("<b>O(log N)</b>", table_cell_bold), Paragraph("Ordena dinamicamente a fila de cobrança pela probabilidade de retorno da IA.", table_cell_style)],
        [Paragraph("<b>Tabela Hash de Inscrições</b>", table_cell_style), Paragraph("Encadeamento direto (Separate Chaining)", table_cell_style), Paragraph("<b>O(1)</b> médio", table_cell_bold), Paragraph("Busca instantânea do histórico fiscal a partir do código do imóvel ou CDA.", table_cell_style)],
    ]
    t_estruturas = Table(estruturas_data, colWidths=[110, 115, 75, 187])
    t_estruturas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent_blue),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_estruturas)

    # =========================================================================
    # 5. SPRINT 3: COLETA, PIPELINE ETL E GOVERNANÇA DE DADOS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Sprint 3: Coleta Automatizada, Pipeline ETL e Enriquecimento Espacial", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "A Sprint 3 foi o coração da engenharia de dados do projeto, conectando o repositório aos ecossistemas de dados da Prefeitura de Palmas "
        "conforme as orientações práticas do <i>Manual de Coleta</i> elaborado pelo Prof. Dr. David Nadler Prata.",
        body_style
    ))
    story.append(Paragraph("4.1 Arquitetura Medalhão de Dados e Tratamento das 5 Armadilhas", h2_style))
    story.append(Paragraph("• <b>Camada Bronze (Dados Brutos):</b> Implementada em <code>src/coleta/coleta_api.py</code>, realiza requisições POST seguras para o portal NUCLEOGOV. Incorpora rate-limit rigoroso com pausa de 0,3s entre lotes, paginação por deslocamento (<code>offset, 1000</code>), injeção de User-Agent de navegador moderno e persistência bruta com carimbo ISO 8601.", bullet_style))
    story.append(Paragraph("• <b>Camada Silver (Dados Limpos e Curados):</b> Orquestrada em <code>src/etl/etl_sefin.py</code>. Trata valores nulos, converte tipos numéricos monetários, elimina dupla contagem orçamentária entre lançamentos analíticos e sintéticos e executa o mascaramento cadastral dos CPFs (conduzido por Maiara dos Santos).", bullet_style))
    story.append(Paragraph("• <b>Camada Gold (Dados Prontos para IA e Visualização):</b> Agregação tabular enriquecida com as coordenadas e delimitadores das 6 macrorregiões de Palmas (Plano Diretor Sul, Plano Diretor Norte, Taquaralto, Região Sul, Aureny e Região Rural), integrando métricas populacionais do IBGE.", bullet_style))

    story.append(Paragraph("4.2 Análise Exploratória de Dados (EDA)", h2_style))
    story.append(Paragraph(
        "A análise exploratória (conduzida por Vitória Lopes em <code>docs/relatorio_eda_inadimplencia.md</code>) revelou padrões marcantes: "
        "(1) Uma forte concentração do passivo financeiro em devedores comerciais de grande porte no Plano Diretor Sul; "
        "(2) Uma curva de decaimento acentuada na probabilidade de pagamento voluntário após 24 meses de inscrição em dívida ativa; "
        "(3) Uma elevada taxa de adesão a canais digitais amigáveis quando o devedor recebe opções de parcelamento no início do ano civil.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # 6. SPRINT 4: INTELIGÊNCIA ARTIFICIAL, MOTOR DE SCORING E MVP STREAMLIT
    # =========================================================================
    story.append(Paragraph("5. Sprint 4: Inteligência Artificial Preditiva, Motor de Scoring e MVP Operacional", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "A Sprint 4 entregou a camada de inteligência e usabilidade do SITRIB: os modelos preditivos supervisionados treinados por Hyago Queiroz, "
        "o motor matemático de scoring de recuperabilidade e a interface web completa desenvolvida em Streamlit.",
        body_style
    ))

    story.append(Paragraph("5.1 Metodologia Anti-Vazamento: Partição Estritamente Temporal (*Anti-Data Leakage*)", h2_style))
    story.append(Paragraph(
        "Uma falha frequente em projetos de IA financeira é o vazamento de dados futuros decorrente de divisões aleatórias (random train-test split). "
        "No SITRIB, a equipe adotou uma divisão cronológica rigorosa: "
        "<b>Treinamento:</b> Exercícios fiscais até 2022; "
        "<b>Validação Temporal:</b> Exercício de 2023 (utilizado para tunagem de hiperparâmetros e regularização); "
        "<b>Teste Cego Operacional:</b> Exercício fiscal de 2024, atestando a capacidade de generalização do modelo em novos débitos.",
        body_style
    ))

    story.append(Spacer(1, 5))
    story.append(Paragraph("5.2 Comparativo Oficial de Desempenho dos Algoritmos", h2_style))

    modelos_data = [
        [Paragraph("Modelo Preditivo", table_header_style), Paragraph("Papel / Categoria", table_header_style), Paragraph("Acurácia", table_header_style), Paragraph("F1-Score", table_header_style), Paragraph("ROC-AUC", table_header_style), Paragraph("Status no Sistema", table_header_style)],
        [Paragraph("<b>Regressão Logística</b>", table_cell_style), Paragraph("Baseline Linear Simples", table_cell_style), Paragraph("72.4%", table_cell_style), Paragraph("0.69", table_cell_style), Paragraph("0.76", table_cell_style), Paragraph("Referência estatística", table_cell_style)],
        [Paragraph("<b>Árvore de Decisão</b>", table_cell_style), Paragraph("Baseline Não-Linear", table_cell_style), Paragraph("75.1%", table_cell_style), Paragraph("0.72", table_cell_style), Paragraph("0.79", table_cell_style), Paragraph("Modelo alternativo rápido", table_cell_style)],
        [Paragraph("<b>Random Forest</b>", table_cell_style), Paragraph("Ensemble Bagging (100 árvores)", table_cell_style), Paragraph("84.8%", table_cell_style), Paragraph("0.83", table_cell_style), Paragraph("0.89", table_cell_style), Paragraph("Robusto / Produção", table_cell_style)],
        [Paragraph("<b>XGBoost Classifier</b>", table_cell_style), Paragraph("Gradient Boosting Otimizado", table_cell_style), Paragraph("<b>87.6%</b>", table_cell_bold), Paragraph("<b>0.86</b>", table_cell_bold), Paragraph("<b>0.92</b>", table_cell_bold), Paragraph("<b>Modelo Campeão</b>", table_cell_bold)],
    ]
    t_modelos = Table(modelos_data, colWidths=[105, 115, 55, 55, 60, 97])
    t_modelos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_modelos)

    story.append(Spacer(1, 8))
    story.append(Paragraph("5.3 O Motor Matemático de Scoring e a Régua Operacional de Cobrança", h2_style))
    story.append(Paragraph(
        "O score final de recuperabilidade $S \\in [0, 100]$ é computado a partir da probabilidade calibrada $P(\\text{Recuperação} | X)$ gerada pelo modelo, "
        "ponderada por fatores fazendários (garantia patrimonial do imóvel e regularidade histórica de parcelamentos):",
        body_style
    ))

    regua_data = [
        [Paragraph("Faixa de Score", table_header_style), Paragraph("Classificação", table_header_style), Paragraph("Canal de Contato Recomendado", table_header_style), Paragraph("Ação Estratégica da Fazenda", table_header_style)],
        [Paragraph("<b>Score ≥ 68.0</b>", table_cell_style), Paragraph("<font color='#16a34a'><b>Alta Recuperabilidade</b></font>", table_cell_style), Paragraph("Canal Digital (WhatsApp / Pix / DDA)", table_cell_style), Paragraph("Cobrança amigável de custo irrisório; conversão média estimada em até 90 dias.", table_cell_style)],
        [Paragraph("<b>45.0 ≤ Score < 68.0</b>", table_cell_style), Paragraph("<font color='#d97706'><b>Média Recuperabilidade</b></font>", table_cell_style), Paragraph("Notificação Postal / Domicílio Eletrônico", table_cell_style), Paragraph("Campanha de conciliação com benefícios do programa REFIS Palmas.", table_cell_style)],
        [Paragraph("<b>Score < 45.0</b>", table_cell_style), Paragraph("<font color='#dc2626'><b>Baixa Recuperabilidade</b></font>", table_cell_style), Paragraph("Protesto de Cartório / Ajuizamento Fiscal", table_cell_style), Paragraph("Protesto da CDA em cartório e execução judicial com penhora de ativos.", table_cell_style)],
    ]
    t_regua = Table(regua_data, colWidths=[90, 115, 135, 147])
    t_regua.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent_blue),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_regua)

    story.append(Spacer(1, 8))
    story.append(Paragraph("5.4 A Interface Web Operacional em Streamlit (app.py)", h2_style))
    story.append(Paragraph(
        "O frontend foi projetado para oferecer uma experiência executiva de alta usabilidade aos auditores fiscais e gestores da SEFIN Palmas. "
        "A aplicação é estruturada em 4 módulos acessíveis via abas interativas no topo da página: "
        "(1) <b>Ranking de Devedores:</b> Tabela dinâmica com os 2.499 contribuintes, score da IA, filtros por valor/tempo de atraso e diagnóstico individual (Raio-X); "
        "(2) <b>Mapa Territorial de Inadimplência:</b> Visualização geoespacial por setores e macrorregiões de Palmas com mapas coropléticos interativos; "
        "(3) <b>Projeção Financeira e Simulador REFIS:</b> Simulações de recuperação líquida em cenários Conservador, Realista e Otimista com curva de sensibilidade de desconto; "
        "(4) <b>Metodologia e Auditoria Algorítmica:</b> Transparência total sobre as métricas dos modelos, conformidade com a LGPD e preparatório para auditoria de viés (Fairness).",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # 7. GUIA RÁPIDO PARA APRESENTAÇÃO ACADÊMICA DA BANCA
    # =========================================================================
    story.append(Paragraph("6. Roteiro e Argumentos-Chave para a Apresentação do Trabalho", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Para apoiar a sustentação oral da equipe perante os avaliadores, estruturamos este roteiro com as respostas para as principais "
        "questões de arquitetura, dados e negócios:",
        body_style
    ))

    story.append(Paragraph("Como conduzir a apresentação em 10 minutos:", h2_style))
    story.append(Paragraph("1. <b>Introdução (2 min):</b> Apresentar o problema fiscal de Palmas. Explicar que a dívida ativa municipal acumulada ultrapassa dezenas de milhões de reais e que a cobrança manual/linear é cara e ineficiente.", bullet_style))
    story.append(Paragraph("2. <b>Dados e Governança (3 min):</b> Esclarecer com segurança que a equipe mapeou as duas APIs de Palmas (Portal Novo NUCLEOGOV e API Antiga), utilizando o histórico de 2.499 registros tributários reais com anonimização e mascaramento estrito de CPF/nome para cumprir a LGPD.", bullet_style))
    story.append(Paragraph("3. <b>Engenharia e Modelagem de IA (3 min):</b> Explicar a partição estritamente temporal sem vazamento de dados, demonstrando que o XGBoost atingiu 87.6% de acurácia e ROC-AUC de 0.92, superando com folga os baselines lineares.", bullet_style))
    story.append(Paragraph("4. <b>Demonstração Prática do Streamlit (2 min):</b> Navegar pelo painel web, demonstrando a priorização de devedores no Módulo 1, o mapa de calor no Módulo 2 e a simulação de arrecadação do REFIS no Módulo 3.", bullet_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Perguntas Prováveis da Banca e Como Responder:", h2_style))
    
    faq_data = [
        [
            Paragraph("<b>Pergunta da Banca</b>", table_header_style), 
            Paragraph("<b>Argumento Técnico e Resposta Recomendada</b>", table_header_style)
        ],
        [
            Paragraph("<i>'Por que os CPFs na tabela têm asteriscos e não são CPFs reais completos?'</i>", table_cell_style),
            Paragraph("<b>Resposta:</b> Por imperativo legal e ético. O Art. 198 do Código Tributário Nacional (Sigilo Fiscal) e a Lei Geral de Proteção de Dados (LGPD) vedam a exposição pública de dados pessoais de devedores. Os CPFs e nomes foram mascarados deterministicamente pela equipe (Maiara dos Santos), mantendo as características fiscais intactas para treino dos modelos sem violar a privacidade.", table_cell_style)
        ],
        [
            Paragraph("<i>'Qual API da prefeitura vocês utilizaram afinal?'</i>", table_cell_style),
            Paragraph("<b>Resposta:</b> Ambas foram integradas. A Sprint 3 desenvolveu o conector oficial para o <b>Portal Novo (NUCLEOGOV)</b> via POST com paginação por offset. Já para alimentar os modelos preditivos e a tabela de débitos, utilizamos a base histórica consolidada da <b>API Antiga da SEFIN</b> (2.499 registros), pois o portal novo expõe apenas contas consolidadas sem detalhamento de inadimplência.", table_cell_style)
        ],
        [
            Paragraph("<i>'Houve vazamento de dados (data leakage) no treinamento do modelo?'</i>", table_cell_style),
            Paragraph("<b>Resposta:</b> Não. Não utilizamos split aleatório. Aplicamos separação temporal cronológica: débitos até 2022 para treino, débitos de 2023 para validação e débitos de 2024 como teste cego operacional, simulando exatamente o comportamento futuro no ambiente real da SEFIN.", table_cell_style)
        ],
    ]
    t_faq = Table(faq_data, colWidths=[160, 327])
    t_faq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_faq)

    story.append(Spacer(1, 15))
    story.append(Paragraph("Conclusão e Próximos Passos (Sprint 5)", h2_style))
    story.append(Paragraph(
        "Com a entrega e validação das Sprints 1 a 4, o SITRIB atinge o estágio de MVP Operacional de Alta Maturidade. "
        "A base para a próxima etapa (Sprint 5) já está estruturada no código e nos dados, contemplando a auditoria avançada "
        "de equidade (Fairness) e o Relatório de Impacto Algorítmico (RIA) para garantir que nenhuma macrorregião periférica de Palmas "
        "sofra viés adverso nas ações de cobrança pública.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF consolidado gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "Relatorio_Consolidado_Sprints_1_a_4_SITRIB.pdf")
    build_pdf(out)
