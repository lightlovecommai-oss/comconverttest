from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 顏色定義
ORANGE = HexColor('#e8734a')
GREEN = HexColor('#5DCAA5')
BLUE = HexColor('#378ADD')
GOLD = HexColor('#c8a84b')
DARK = HexColor('#2d1f0f')
MID = HexColor('#6b4c30')
LIGHT = HexColor('#a08060')
BG = HexColor('#fdf8f3')
BORDER = HexColor('#e8ddd2')
LIGHT_BG = HexColor('#f0e4d4')

# 字型設定
font_paths = [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/Library/Fonts/Arial Unicode MS.ttf',
]
font_name = 'Helvetica'
for fp in font_paths:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont('CJK', fp))
            pdfmetrics.registerFont(TTFont('CJK-Bold', fp))
            font_name = 'CJK'
            break
        except:
            continue

W, H = A4

def make_styles(fn):
    return {
        'title': ParagraphStyle('title', fontName=fn, fontSize=22, textColor=DARK, spaceAfter=4, alignment=TA_CENTER, leading=30),
        'subtitle': ParagraphStyle('subtitle', fontName=fn, fontSize=12, textColor=LIGHT, spaceAfter=16, alignment=TA_CENTER),
        'h1': ParagraphStyle('h1', fontName=fn, fontSize=15, textColor=DARK, spaceBefore=16, spaceAfter=6, leading=22),
        'h2': ParagraphStyle('h2', fontName=fn, fontSize=12, textColor=ORANGE, spaceBefore=10, spaceAfter=4, leading=18),
        'body': ParagraphStyle('body', fontName=fn, fontSize=10, textColor=MID, spaceAfter=4, leading=17),
        'small': ParagraphStyle('small', fontName=fn, fontSize=9, textColor=LIGHT, spaceAfter=3, leading=14),
        'tag': ParagraphStyle('tag', fontName=fn, fontSize=9, textColor=ORANGE, spaceAfter=3),
        'center': ParagraphStyle('center', fontName=fn, fontSize=10, textColor=MID, alignment=TA_CENTER, leading=16),
        'formula': ParagraphStyle('formula', fontName=fn, fontSize=13, textColor=ORANGE, alignment=TA_CENTER, spaceBefore=6, spaceAfter=6, leading=20),
        'caption': ParagraphStyle('caption', fontName=fn, fontSize=8, textColor=LIGHT, alignment=TA_CENTER),
        'white': ParagraphStyle('white', fontName=fn, fontSize=10, textColor=white, leading=16),
        'white_bold': ParagraphStyle('white_bold', fontName=fn, fontSize=12, textColor=white, leading=18),
        'label': ParagraphStyle('label', fontName=fn, fontSize=8, textColor=LIGHT, spaceAfter=2),
    }

def build_pdf():
    output_path = '/Users/ivor/comconvertai/comconverttest/溝通變現框架.pdf'
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=18*mm,
        leftMargin=18*mm,
        topMargin=16*mm,
        bottomMargin=16*mm,
    )
    S = make_styles(font_name)
    story = []

    # ── 封面區 ──────────────────────────────────────────────
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph('溝通變現框架', S['title']))
    story.append(Paragraph('合作夥伴內部說明文件', S['subtitle']))
    story.append(HRFlowable(width='100%', thickness=1, color=BORDER, spaceAfter=8))
    story.append(Paragraph('本文件說明「溝通變現測驗」背後的完整邏輯框架，包含核心定位、ATPI 四維度、公式推導、變現路徑分類，以及三階課程對應。', S['body']))
    story.append(Spacer(1, 10*mm))

    # ── 一、核心定位 ────────────────────────────────────────
    story.append(Paragraph('一、核心定位', S['h1']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))

    core = Table(
        [[Paragraph('測驗幫使用者回答三件事', S['h2'])],
         [Paragraph('1. 診斷你的溝通能力（ATPI 四維度）', S['body'])],
         [Paragraph('2. 找出你第一條 / 最容易的天賦變現路徑', S['body'])],
         [Paragraph('3. 讓你意識到「錢漏在哪裡」——能力有了，但流程沒跑通', S['body'])],
        ],
        colWidths=[W - 36*mm],
    )
    core.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BACKGROUND', (0,1), (-1,-1), BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(core)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph('關鍵前提', S['h2']))
    story.append(Paragraph('台灣的講師、專業技術人、1人公司老闆，通常 P（專業力）已經很高，但 A（吸引力）最弱、I（推進力）不足。這不是能力問題，是流程問題——他們沒有意識到需要拆解自己的成交流程，所以能力再強也是靠運氣在賺錢。', S['body']))
    story.append(Spacer(1, 6*mm))

    # ── 二、ATPI 四維度 ─────────────────────────────────────
    story.append(Paragraph('二、ATPI 四個維度', S['h1']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))
    story.append(Paragraph('ATPI 是一個不可分割的成交流程，不是四個獨立分數。任何一段斷掉，整條流程就失敗。', S['body']))
    story.append(Spacer(1, 3*mm))

    flow_data = [
        [
            Paragraph('A\nAttract\n吸引力', S['center']),
            Paragraph('>', S['center']),
            Paragraph('T\nTrust\n信任力', S['center']),
            Paragraph('>', S['center']),
            Paragraph('P\nProfessional\n專業力', S['center']),
            Paragraph('>', S['center']),
            Paragraph('I\nImpact\n推進力', S['center']),
        ],
        [
            Paragraph('讓對方想靠近、想繼續聽', S['small']),
            Paragraph('', S['small']),
            Paragraph('讓對方打開心房、說真話', S['small']),
            Paragraph('', S['small']),
            Paragraph('讓對方覺得你真的懂他', S['small']),
            Paragraph('', S['small']),
            Paragraph('在對的時機推一把讓對方行動', S['small']),
        ],
    ]
    cw = (W - 36*mm) / 7
    flow_table = Table(flow_data, colWidths=[cw*1.4, cw*0.4, cw*1.4, cw*0.4, cw*1.4, cw*0.4, cw*1.4])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), HexColor('#fff3ee')),
        ('BACKGROUND', (2,0), (2,-1), HexColor('#eefaf6')),
        ('BACKGROUND', (4,0), (4,-1), HexColor('#eef4ff')),
        ('BACKGROUND', (6,0), (6,-1), HexColor('#fdf8ee')),
        ('TEXTCOLOR', (0,0), (0,0), ORANGE),
        ('TEXTCOLOR', (2,0), (2,0), GREEN),
        ('TEXTCOLOR', (4,0), (4,0), BLUE),
        ('TEXTCOLOR', (6,0), (6,0), GOLD),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOX', (0,0), (0,-1), 0.5, BORDER),
        ('BOX', (2,0), (2,-1), 0.5, BORDER),
        ('BOX', (4,0), (4,-1), 0.5, BORDER),
        ('BOX', (6,0), (6,-1), 0.5, BORDER),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('重要認知：ATPI 是場景依賴的', S['h2']))
    scene_data = [
        [Paragraph('場景', S['label']), Paragraph('特性', S['label']), Paragraph('影響', S['label'])],
        [Paragraph('1 對 1', S['body']), Paragraph('有眼神、語氣、即時回應', S['body']), Paragraph('A、I 可以充分發揮', S['body'])],
        [Paragraph('群體現場', S['body']), Paragraph('單向為主，但有現場感', S['body']), Paragraph('A、I 主導', S['body'])],
        [Paragraph('社群內容', S['body']), Paragraph('只剩文字或影片，無互動信號', S['body']), Paragraph('A、I 容易失效', S['body'])],
    ]
    scene_table = Table(scene_data, colWidths=[(W-36*mm)*0.2, (W-36*mm)*0.4, (W-36*mm)*0.4])
    scene_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BACKGROUND', (0,1), (-1,-1), BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(scene_table)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('同一個人在 1v1 場合 A、I 可能很強，但放到社群內容就失效——不是能力不夠，是還沒學會「媒介轉譯」，把能力搬到那個場景裡。', S['body']))
    story.append(Spacer(1, 6*mm))

    # ── 三、公式 ────────────────────────────────────────────
    story.append(Paragraph('三、溝通變現潛力公式', S['h1']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))

    formula_box = Table(
        [[Paragraph('溝通變現潛力 = A x T x P x I', S['formula'])],
         [Paragraph('（各維度 0-100，潛力指數 0-10000）', S['caption'])],
        ],
        colWidths=[W - 36*mm],
    )
    formula_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#fff3ee')),
        ('BOX', (0,0), (-1,-1), 1, ORANGE),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(formula_box)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('為什麼用乘法？', S['h2']))
    story.append(Paragraph('乘法代表任何一個維度趨近於零，整體潛力就崩潰。這符合真實成交流程的邏輯：A 不夠，沒有人進來聽你說；T 不夠，對方不願意說出真實需求；P 不夠，對方不相信你能幫他；I 不夠，前面三步都做對了，對方還是沒有採取行動。', S['body']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph('收入 vs 潛力的差距', S['h2']))
    gap_data = [
        [Paragraph('現有收入', S['label']), Paragraph('溝通變現潛力', S['label']), Paragraph('代表的意義', S['label'])],
        [Paragraph('低', S['body']), Paragraph('高', S['body']), Paragraph('能力有了，但 SOP 還沒跑通，錢都漏掉了', S['body'])],
        [Paragraph('高', S['body']), Paragraph('低', S['body']), Paragraph('靠組織品牌或運氣在賺，換環境可能撐不住', S['body'])],
        [Paragraph('高', S['body']), Paragraph('高', S['body']), Paragraph('能力和流程都到位，可以進一步規模化', S['body'])],
    ]
    gap_table = Table(gap_data, colWidths=[(W-36*mm)*0.2, (W-36*mm)*0.25, (W-36*mm)*0.55])
    gap_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BACKGROUND', (0,1), (-1,-1), BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(gap_table)
    story.append(Spacer(1, 6*mm))

    # ── 四、四種強項類型 ────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('四、四種強項類型與天賦變現路徑', S['h1']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))
    story.append(Paragraph('每個人的強項決定他自然跑的路徑，但強項也會造成他的盲點。', S['body']))
    story.append(Spacer(1, 3*mm))

    types = [
        (ORANGE, 'A 強・吸引型', '社群、演講、異業合作', '吸引到但成交不了\n第二條路：演講課程（補 I）'),
        (GREEN,  'T 強・關係型', '介紹變現、顧問、長期客戶', '客戶喜歡但不買單\n第二條路：社群私域（補 A）'),
        (BLUE,   'P 強・權威型', '企業培訓、顧問、技術服務', '說了很多但沒有行動\n第二條路：線上課程品牌（補 A）'),
        (GOLD,   'I 強・推進型', '演講收單、直銷、業務', '推太快信任不夠退單多\n第二條路：1v1 高單價顧問（補 T）'),
    ]
    for color, name, paths, blocks in types:
        row = Table(
            [[
                Paragraph(name, ParagraphStyle('th', fontName=font_name, fontSize=11, textColor=white, leading=16)),
            ],[
                Table([
                    [Paragraph('自然路徑', S['label']), Paragraph('常見卡點與第二條路', S['label'])],
                    [Paragraph(paths, S['body']), Paragraph(blocks, S['body'])],
                ], colWidths=[(W-36*mm-24)*0.4, (W-36*mm-24)*0.6],
                style=TableStyle([
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                ])),
            ]],
            colWidths=[W - 36*mm],
        )
        row.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), color),
            ('BACKGROUND', (0,1), (-1,1), BG),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER),
            ('TOPPADDING', (0,0), (-1,0), 8),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('LEFTPADDING', (0,0), (-1,0), 12),
            ('TOPPADDING', (0,1), (-1,1), 8),
            ('BOTTOMPADDING', (0,1), (-1,1), 8),
            ('LEFTPADDING', (0,1), (-1,1), 12),
            ('RIGHTPADDING', (0,1), (-1,1), 12),
        ]))
        story.append(row)
        story.append(Spacer(1, 4*mm))

    story.append(Spacer(1, 2*mm))

    # ── 五、變現路徑分類 ────────────────────────────────────
    story.append(Paragraph('五、變現路徑分類', S['h1']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))
    story.append(Paragraph('根據目標客群（講師、專業技術人、1人公司老闆）整理出的主要變現路徑，按天花板係數排列。', S['body']))
    story.append(Spacer(1, 3*mm))

    path_data = [
        [Paragraph('路徑', S['label']), Paragraph('主要驅動維度', S['label']), Paragraph('天花板係數', S['label']), Paragraph('說明', S['label'])],
        [Paragraph('社群／影響力變現', S['body']), Paragraph('A + I', S['body']), Paragraph('x5.0', ParagraphStyle('bold', fontName=font_name, fontSize=10, textColor=ORANGE)), Paragraph('自媒體、課程，規模最大', S['body'])],
        [Paragraph('演講現場收單', S['body']), Paragraph('A + I', S['body']), Paragraph('x3.5', ParagraphStyle('bold', fontName=font_name, fontSize=10, textColor=ORANGE)), Paragraph('一次觸及多人，現場成交', S['body'])],
        [Paragraph('關係變現', S['body']), Paragraph('T + P', S['body']), Paragraph('x3.0', S['body']), Paragraph('顧問、coaching，高單價', S['body'])],
        [Paragraph('介紹變現', S['body']), Paragraph('T + P', S['body']), Paragraph('x1.5', S['body']), Paragraph('轉介紹，時間天花板低', S['body'])],
        [Paragraph('企業培訓 / B2B', S['body']), Paragraph('T + P', S['body']), Paragraph('x3.0', S['body']), Paragraph('賣給公司，單次高但頻率低', S['body'])],
        [Paragraph('募資變現', S['body']), Paragraph('A + T + I', S['body']), Paragraph('—', S['body']), Paragraph('群眾預購，需要信任 + 吸引力', S['body'])],
    ]
    path_table = Table(path_data, colWidths=[(W-36*mm)*0.28, (W-36*mm)*0.22, (W-36*mm)*0.15, (W-36*mm)*0.35])
    path_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BACKGROUND', (0,1), (-1,2), HexColor('#fff3ee')),
        ('BACKGROUND', (0,3), (-1,-1), BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(path_table)
    story.append(Spacer(1, 6*mm))

    # ── 六、SOP 層 ──────────────────────────────────────────
    story.append(Paragraph('六、為什麼「SOP 層」不用測驗？', S['h1']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))

    sop_data = [
        [Paragraph('SOP Level', S['label']), Paragraph('狀態描述', S['label']), Paragraph('對應課程', S['label'])],
        [Paragraph('Level 0', S['body']), Paragraph('完全沒意識，不知道自己需要流程', S['body']), Paragraph('1 階', S['body'])],
        [Paragraph('Level 1', S['body']), Paragraph('有模糊習慣，沒有系統，時通時不通', S['body']), Paragraph('1 階 + 2 階', S['body'])],
        [Paragraph('Level 2', S['body']), Paragraph('一條路徑跑通，但單一來源，很脆弱', S['body']), Paragraph('2 階', S['body'])],
        [Paragraph('Level 3+', S['body']), Paragraph('想放大規模，從 1v1 到 1vN', S['body']), Paragraph('3 階', S['body'])],
    ]
    sop_table = Table(sop_data, colWidths=[(W-36*mm)*0.18, (W-36*mm)*0.55, (W-36*mm)*0.27])
    sop_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BACKGROUND', (0,1), (-1,-1), BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(sop_table)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('來做測驗的人，幾乎沒有意識到自己需要系統化流程——所以 SOP 不需要在問卷裡測，而是在結果頁用文案讓他意識到：「你的能力值這個錢，但你的流程讓你少賺了。」', S['body']))
    story.append(Spacer(1, 6*mm))

    # ── 七、三階課程 ────────────────────────────────────────
    story.append(Paragraph('七、三階課程對應', S['h1']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))

    stages = [
        (ORANGE, '1 階', '溝通能力', '理解 ATPI 四個維度，找出自己的天賦強項與成交斷點。\n適合：所有人都需要，是進入 2 階的基礎。'),
        (GREEN,  '2 階', '1 對 1 變現 SOP', '把 A → T → P → I 串成一條完整的成交流程，讓賺錢變成設計而非運氣。\n適合：ATPI 具備基礎，想把第一條路徑跑穩，或想建立第二條路徑的人。'),
        (BLUE,   '3 階', '1 對 N 演講現場收單', '把 1v1 的成交能力放大到 1vN，每次演講或活動都能現場收單。\n適合：已有流程、想規模化的講師或培訓師。'),
    ]
    for color, num, name, desc in stages:
        row = Table([[
            Table([[Paragraph(num, ParagraphStyle('num', fontName=font_name, fontSize=18, textColor=white, alignment=TA_CENTER))]], colWidths=[16*mm],
                  style=TableStyle([('BACKGROUND', (0,0), (-1,-1), color), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)])),
            Table([
                [Paragraph(name, ParagraphStyle('sn', fontName=font_name, fontSize=12, textColor=DARK, leading=16))],
                [Paragraph(desc, S['body'])],
            ], colWidths=[W - 36*mm - 16*mm - 4*mm],
            style=TableStyle([('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('LEFTPADDING', (0,0), (-1,-1), 10)])),
        ]], colWidths=[16*mm, W - 36*mm - 16*mm])
        row.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, BORDER),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(row)
        story.append(Spacer(1, 4*mm))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('* 公域流量（社群自然流量）目前不在課程範疇內，誠實告知學員。', S['small']))
    story.append(Spacer(1, 6*mm))

    # ── 八、測驗結果頁邏輯 ──────────────────────────────────
    story.append(Paragraph('八、測驗結果頁邏輯', S['h1']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))

    result_data = [
        [Paragraph('區塊', S['label']), Paragraph('內容', S['label']), Paragraph('目的', S['label'])],
        [Paragraph('第一區', S['body']), Paragraph('溝通變現潛力指數（大數字）', S['body']), Paragraph('視覺衝擊，秒懂自己的位置', S['body'])],
        [Paragraph('第二區', S['body']), Paragraph('ATPI 四個分數 + 雷達圖', S['body']), Paragraph('看出強弱分布', S['body'])],
        [Paragraph('第三區', S['body']), Paragraph('你的溝通能力分析（最弱維度）', S['body']), Paragraph('戳出成交斷點，製造危機感', S['body'])],
        [Paragraph('第四區', S['body']), Paragraph('你最容易成功的天賦變現路徑', S['body']), Paragraph('給場景描繪，讓人有共鳴', S['body'])],
        [Paragraph('第五區', S['body']), Paragraph('預約諮詢按鈕', S['body']), Paragraph('低門檻行動，聊完再導課程', S['body'])],
    ]
    result_table = Table(result_data, colWidths=[(W-36*mm)*0.15, (W-36*mm)*0.42, (W-36*mm)*0.43])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('BACKGROUND', (0,1), (-1,-1), BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 8*mm))

    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))
    story.append(Paragraph('測驗線上網址：https://lightlovecommai-oss.github.io/comconverttest/', S['small']))

    doc.build(story)
    print(f'PDF 已產生：{output_path}')

build_pdf()
