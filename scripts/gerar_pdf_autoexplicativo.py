import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
            return  # Capa limpa
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Cabeçalho
        self.drawString(54, 800, "SITRIB-Palmas • Guia Autoexplicativo do Projeto (Sprints 1 a 4)")
        self.drawRightString(541, 800, "UFT / BIINAR • SEFIN Palmas-TO")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792)
        
        # Rodapé
        self.line(54, 45, 541, 45)
        self.drawString(54, 32, "Documento didático e simplificado para apresentação e consulta de qualquer leitor")
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
    
    primary_color = colors.HexColor("#0f172a")    # Azul ardósia escuro
    accent_blue = colors.HexColor("#1e40af")      # Azul real
    dark_neutral = colors.HexColor("#1e293b")
    light_bg = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")
    highlight_box = colors.HexColor("#eff6ff")
    warning_box = colors.HexColor("#fefce8")
    success_box = colors.HexColor("#f0fdf4")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=accent_blue,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=dark_neutral,
        spaceAfter=5,
        alignment=4
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    box_title = ParagraphStyle(
        'BoxTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=3
    )

    box_text = ParagraphStyle(
        'BoxText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#1e3a8a")
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=primary_color
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    story = []

    # =========================================================================
    # CAPA / CABEÇALHO DO DOCUMENTO
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("UNIVERSIDADE FEDERAL DO TOCANTINS (UFT) • BIINAR", ParagraphStyle('Uni', fontName='Helvetica-Bold', fontSize=9.5, leading=11, textColor=colors.HexColor("#64748b"))))
    story.append(Paragraph("PROJETO INTEGRADOR DO EIXO II • SECRETARIA MUNICIPAL DE FINANÇAS DE PALMAS (SEFIN)", ParagraphStyle('SubUni', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor("#94a3b8"))))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2.5, color=accent_blue, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph("Guia Autoexplicativo do Sistema SITRIB (Palmas-TO)", title_style))
    story.append(Paragraph("Tudo sobre o projeto, as 4 etapas, a usabilidade e a escolha da base histórica explicados em texto simples para qualquer leitor", subtitle_style))
    story.append(Spacer(1, 6))

    # Box Explicativo Inicial
    intro_box_data = [[
        Paragraph("<b>OBJETIVO DESTE GUIA:</b>", box_title),
    ], [
        Paragraph(
            "Este guia foi escrito especialmente para que <b>qualquer pessoa, mesmo sem conhecimento técnico de computação ou matemática</b>, "
            "consiga ler, entender perfeitamente o sistema, saber como usá-lo na prática e apresentar o trabalho com total segurança. "
            "Explicamos de ponta a ponta o problema real de Palmas, quem fez cada parte, por que usamos a API Antiga, como funciona a usabilidade "
            "da tela e o resumo completo das 4 Sprints.",
            box_text
        )
    ]]
    t_intro = Table(intro_box_data, colWidths=[487])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), highlight_box),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93c5fd")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 10))

    # Tabela da Equipe
    story.append(Paragraph("Quem fez o projeto? (A Equipe e o que cada um realizou)", h2_style))
    equipe_humana = [
        [Paragraph("Integrante", table_header), Paragraph("Papel no Projeto", table_header), Paragraph("O que essa pessoa fez no sistema (Em palavras simples)", table_header)],
        [Paragraph("<b>Sofia Barros de Jesus</b>", table_cell), Paragraph("Scrum Master & Eng. de Dados", table_cell), Paragraph("Construiu o banco de dados e o 'cano' que puxa, limpa e organiza todas as informações da prefeitura.", table_cell)],
        [Paragraph("<b>Ludmylla Teixeira</b>", table_cell), Paragraph("Product Owner (Dona do Produto)", table_cell), Paragraph("Definiu as regras do negócio: o que a prefeitura precisa, quem deve ser protegido e como o sistema deve agir.", table_cell)],
        [Paragraph("<b>Vitória Lopes</b>", table_cell), Paragraph("Frontend & Analista de Dados", table_cell), Paragraph("Criou o site interativo onde o usuário mexe na tela (o painel Streamlit) e os mapas coloridos dos bairros de Palmas.", table_cell)],
        [Paragraph("<b>Hyago Herrcolis Queiroz</b>", table_cell), Paragraph("Cientista de Dados (IA)", table_cell), Paragraph("Ensinou o computador a analisar os dados do passado e calcular a 'nota' (score) de quem tem mais chance de pagar.", table_cell)],
        [Paragraph("<b>Maiara dos Santos</b>", table_cell), Paragraph("Governança e Proteção de Dados", table_cell), Paragraph("Garantiu que o CPF e nome das pessoas fossem protegidos com disfarce (LGPD) e que a IA não fosse preconceituosa.", table_cell)]
    ]
    t_eq = Table(equipe_humana, colWidths=[110, 115, 262])
    t_eq.setStyle(TableStyle([
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
    story.append(t_eq)

    story.append(Spacer(1, 10))
    story.append(Paragraph("1. O que é o SITRIB e qual o problema real que ele resolve em Palmas?", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "A Prefeitura de Palmas possui dezenas de milhões de reais em impostos municipais atrasados que não foram pagos "
        "(principalmente IPTU de casas e lotes, ISS de empresas e taxas de licença). Quando um imposto vence e não é pago, ele vira o que chamamos de <b>Dívida Ativa</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Como a Prefeitura cobrava antigamente:</b> A prefeitura tentava cobrar todo mundo de forma igual, mandando cartas padronizadas ou abrindo processos "
        "na Justiça contra qualquer devedor. Só que abrir um processo judicial custa muito caro para os cofres públicos (em média R$ 4.500 por processo!). "
        "Muitas vezes a pessoa cobrada é uma família de baixa renda que não tem como pagar, enquanto grandes empresas com dinheiro em caixa não pagam de propósito "
        "porque sabem que o processo demora anos na Justiça.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Como o SITRIB resolve isso:</b> O SITRIB é um sistema inteligente que calcula uma <b>nota de 0 a 100</b> para cada dívida, chamada <b>Score de Recuperabilidade</b>. "
        "Essa nota diz: <i>'Qual é a probabilidade real dessa pessoa ou empresa pagar se a prefeitura entrar em contato pelo canal certo?'</i>. "
        "Com isso, a prefeitura economiza dinheiro público, não cobra na justiça famílias humildes e arrecada mais onde realmente é viável receber.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # SEÇÃO 2: POR QUE ESCOLHEMOS A API ANTIGA E OS CPFS COM ASTERISCOS
    # =========================================================================
    story.append(Paragraph("2. Por que Escolhemos a API Antiga e Como Ficam os CPFs?", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "Essa é uma das dúvidas mais comuns de quem avalia o projeto. Veja a justificativa técnica e prática:",
        body_style
    ))

    # Box Verde: Por que a API antiga foi a melhor escolha
    api_escolha_box = [[
        Paragraph("<b>POR QUE ESCOLHEMOS A API ANTIGA DA PREFEITURA?</b>", ParagraphStyle('STH', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#166534"))),
    ], [
        Paragraph(
            "A resposta é simples e direta: <b>a API Antiga foi escolhida porque era a fonte pública MAIS COMPLETA e com a MELHOR AMOSTRA DE DADOS "
            "reais para se trabalhar</b>. A prefeitura tem duas APIs:<br/>"
            "• <b>O Portal Novo (NUCLEOGOV):</b> É o sistema recente, mas ele só publica o total geral de receitas arrecadadas por mês de forma agregada. "
            "Ele não tem os registros individuais de quem deve nem o histórico de dívida caso a caso.<br/>"
            "• <b>A API Antiga (SEFIN Histórico):</b> Continha a base histórica completa com <b>2.499 registros detalhados</b> de lançamentos de dívidas, "
            "arrecadações, tipos de impostos e tempo de atraso em Palmas. Sem essa base histórica detalhada, seria impossível treinar uma Inteligência Artificial "
            "de verdade. Por isso, a API Antiga foi a melhor e mais rica amostra de dados públicos disponível para o projeto.",
            ParagraphStyle('STB', fontName='Helvetica', fontSize=8, leading=12, textColor=colors.HexColor("#166534"))
        )
    ]]
    t_api_box = Table(api_escolha_box, colWidths=[487])
    t_api_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), success_box),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86efac")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_api_box)
    story.append(Spacer(1, 8))

    # Box Amarelo: Proteção de Dados e Asteriscos
    lgpd_box_data = [[
        Paragraph("<b>SEGURANÇA LEGAL E LGPD: POR QUE OS CPFS TÊM ASTERISCOS?</b>", ParagraphStyle('WTH', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#854d0e"))),
    ], [
        Paragraph(
            "No Brasil, o <b>Código Tributário Nacional (Sigilo Fiscal - Art. 198)</b> e a <b>Lei Geral de Proteção de Dados (LGPD)</b> proíbem expor "
            "em público o nome e o CPF de cidadãos com débitos. Para cumprir rigorosamente a lei, a integrante <b>Maiara dos Santos</b> aplicou um disfarce "
            "protetor: substituiu os dígitos do meio dos CPFs por asteriscos (ex: <code>***.123.456-**</code>) e gerou nomes de fantasia protegidos. "
            "<br/><b>O que importa saber:</b> Todos os valores de dinheiro em reais, os juros, os bairros de Palmas e os meses de atraso são <b>100% VERDADEIROS</b>! "
            "Dessa forma, o sistema aprendeu com a realidade de Palmas sem violar a privacidade de nenhum cidadão.",
            ParagraphStyle('WTB', fontName='Helvetica', fontSize=8, leading=12, textColor=colors.HexColor("#854d0e"))
        )
    ]]
    t_lgpd = Table(lgpd_box_data, colWidths=[487])
    t_lgpd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), warning_box),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#facc15")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_lgpd)

    # =========================================================================
    # SEÇÃO 3: USABILIDADE DO SISTEMA (COMO O USUÁRIO OPERA)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Usabilidade do Sistema: Como Qualquer Pessoa Usa o SITRIB?", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "O sistema foi desenvolvido pela <b>Vitória Lopes</b> na ferramenta Streamlit com foco total em <b>usabilidade prática</b>. "
        "Isso significa que um auditor fiscal, secretário de finanças ou qualquer pessoa consegue usar o sistema sem precisar de treinamento técnico:",
        body_style
    ))
    story.append(Paragraph("• <b>Visão Rápida dos Indicadores (No Topo da Tela):</b> Ao abrir o sistema, cinco cartões mostram na hora o panorama geral de Palmas: o volume total em dívida (mais de R$ 35 milhões), quanto pode ser recuperado imediatamente (R$ 9,2 milhões), a quantidade de devedores (2.499), o valor médio de cada dívida e a nota média de facilidade de pagamento.", bullet_style))
    story.append(Paragraph("• <b>Filtros Fáceis na Barra Lateral:</b> Na barra cinza à esquerda, você pode filtrar os dados com cliques simples: escolher o imposto (IPTU, ISS, taxas), escolher a região de Palmas (Centro, Sul, Norte, etc.) e puxar barrinhas deslizantes para filtrar dívidas por valor em reais ou por tempo de atraso.", bullet_style))
    story.append(Paragraph("• <b>Navegação Simples em 4 Abas:</b>", bullet_style))
    story.append(Paragraph("  - <b>Aba 1 (Ranking de Devedores):</b> Mostra a lista ordenada de quem a prefeitura deve cobrar primeiro. Ao clicar em um devedor, o sistema abre um <i>Raio-X</i> explicando o motivo da nota e recomendando o canal exato (WhatsApp, carta ou cartório). Tem um botão para baixar a lista em planilha Excel/CSV.", bullet_style))
    story.append(Paragraph("  - <b>Aba 2 (Mapa de Calor):</b> Mostra mapas coloridos de Palmas onde as cores mais quentes indicam os bairros com mais dinheiro parado.", bullet_style))
    story.append(Paragraph("  - <b>Aba 3 (Simulador REFIS):</b> Permite arrastar uma barrinha de desconto (ex: 70% de desconto nas multas) e o computador calcula na hora quantos milhões de reais vão entrar nos cofres do município.", bullet_style))
    story.append(Paragraph("  - <b>Aba 4 (Auditoria e Metodologia):</b> Mostra a prestação de contas dos algoritmos e disponibiliza o botão para baixar este PDF explicativo com um único clique.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # SEÇÃO 4: RESUMO DAS 4 IMPLEMENTAÇÕES (SPRINTS)
    # =========================================================================
    story.append(Paragraph("4. Resumo das 4 Implementações (O que foi feito em cada Sprint)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("Sprint 1 — O Planejamento e as Regras Humanas", h2_style))
    story.append(Paragraph(
        "Fase de definição do negócio liderada por <b>Ludmylla Teixeira</b>: mapeamos os problemas de Palmas e estabelecemos a regra de ouro: "
        "famílias vulneráveis inscritas no programa <b>IPTU Social</b> (em bairros como Taquaralto, Jardins Aureny e Taquari) jamais devem ser levadas "
        "à Justiça; o sistema recomenda para elas anistia, isenção e parcelamentos simbólicos de até 10% da renda. Já os grandes devedores do Plano Diretor são priorizados.",
        body_style
    ))

    story.append(Paragraph("Sprint 2 — A Organização das Gavetas (Banco de Dados Relacional 3FN)", h2_style))
    story.append(Paragraph(
        "Fase de organização técnica liderada por <b>Sofia Barros</b>: organizamos os dados em 3 tabelas conectadas (Contribuinte, Imóvel e Dívida) para eliminar "
        "duplicidades e erros. Criamos também 3 rotinas ultra-rápidas no computador: um rastreador de bens que descobre quem é dono de vários imóveis na cidade, "
        "uma fila que organiza as dívidas da mais fácil para a mais difícil e uma busca que localiza qualquer imóvel em milissegundos.",
        body_style
    ))

    story.append(Paragraph("Sprint 3 — A Coleta dos Dados e o Mapa de Calor (ETL e EDA)", h2_style))
    story.append(Paragraph(
        "Fase de dados liderada por <b>Sofia Barros, Vitória Lopes e Maiara dos Santos</b>: construímos o robô coletor seguro da prefeitura (respeitando as regras "
        "do Prof. Dr. David Nadler Prata, com pausa de 0,3s para não sobrecarregar os servidores). Dividimos os dados em camadas Bronze (bruto), Silver (limpo e "
        "sem CPFs expostos) e Gold (enriquecido com mapas de Palmas e dados de renda do IBGE). A Vitória gerou os mapas de calor que comprovam onde a dívida se concentra.",
        body_style
    ))

    story.append(Paragraph("Sprint 4 — A Inteligência Artificial e a Tela Interativa (ML e MVP Streamlit)", h2_style))
    story.append(Paragraph(
        "Fase de inteligência e tela liderada por <b>Hyago Queiroz e Vitória Lopes</b>: treinamos o modelo de Inteligência Artificial XGBoost (que atingiu 87,6% "
        "de acurácia, superando todos os métodos antigos). A IA calcula a nota de 0 a 100 e divide os devedores em 3 caminhos práticos:",
        body_style
    ))

    regua_humana = [
        [Paragraph("Nota (Score)", table_header), Paragraph("Facilidade", table_header), Paragraph("Canal Indicado", table_header), Paragraph("Ação Prática da Prefeitura", table_header)],
        [Paragraph("<b>Acima de 68</b>", table_cell_bold), Paragraph("<font color='#16a34a'><b>Alta</b></font>", table_cell), Paragraph("WhatsApp / Pix / DDA", table_cell), Paragraph("Envia código Pix ou boleto no celular. Custo quase zero e a pessoa paga rápido.", table_cell)],
        [Paragraph("<b>De 45 a 68</b>", table_cell_bold), Paragraph("<font color='#d97706'><b>Média</b></font>", table_cell), Paragraph("Carta / Notificação", table_cell), Paragraph("Convida para parcelar com desconto nos juros através do programa REFIS Palmas.", table_cell)],
        [Paragraph("<b>Abaixo de 45</b>", table_cell_bold), Paragraph("<font color='#dc2626'><b>Baixa</b></font>", table_cell), Paragraph("Cartório / Justiça", table_cell), Paragraph("Protesta em cartório e aciona a Procuradoria para penhora de bens de grandes empresas.", table_cell)],
    ]
    t_reg = Table(regua_humana, colWidths=[75, 70, 125, 217])
    t_reg.setStyle(TableStyle([
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
    story.append(t_reg)

    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Roteiro de 10 Minutos para Apresentar o Trabalho", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("<b>Minuto 1 ao 3 (O Problema):</b> Apresente o nome do sistema (SITRIB) e explique que Palmas tem mais de R$ 35 milhões parados em dívida ativa. Explique que o jeito antigo de cobrar na Justiça é caro e prejudica os pobres, e que o SITRIB usa IA para cobrar com inteligência e humanidade.", body_style))
    story.append(Paragraph("<b>Minuto 3 ao 6 (Os Dados e as Leis):</b> Explique com clareza que escolhemos a API Antiga da SEFIN porque ela tinha a amostra de dados públicos mais completa e rica (2.499 registros detalhados), e que a Maiara mascarou os CPFs com asteriscos para respeitar a LGPD e o Sigilo Fiscal, mantendo valores e bairros 100% reais.", body_style))
    story.append(Paragraph("<b>Minuto 6 ao 8 (A Inteligência Artificial):</b> Diga que o Hyago treinou o modelo XGBoost sem vazamento temporal (treinou com anos antigos e testou com anos novos), atingindo 87,6% de acertos. Explique a régua: WhatsApp para quem tem nota alta, REFIS para nota média e cartório para nota baixa.", body_style))
    story.append(Paragraph("<b>Minuto 8 ao 10 (A Demonstração da Tela):</b> Mostre o site Streamlit feito pela Vitória: a lista de devedores, o mapa colorido de Palmas, a simulação de dinheiro entrando com o REFIS e encerre com segurança convidando para perguntas.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Guia autoexplicativo gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "Guia_Autoexplicativo_Sprints_1_a_4_SITRIB.pdf")
    build_pdf(out)
