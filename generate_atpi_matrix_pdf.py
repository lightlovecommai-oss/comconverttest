from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('PingFang', '/Library/Fonts/Arial Unicode.ttf'))

OUTPUT = "/Users/ivor/comconvertai/comconverttest/ATPI場景重要性矩陣.pdf"

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=18*mm, bottomMargin=18*mm
)

ORANGE = colors.HexColor("#e8734a")
TEAL   = colors.HexColor("#5DCAA5")
BLUE   = colors.HexColor("#378ADD")
GOLD   = colors.HexColor("#c8a84b")
DARK   = colors.HexColor("#2d1f0f")
MID    = colors.HexColor("#6b4c30")
LIGHT  = colors.HexColor("#f5ede3")
CREAM  = colors.HexColor("#fdf8f3")
BORDER = colors.HexColor("#e8ddd2")

def ps(size=11, color=DARK, leading=None):
    return ParagraphStyle('x', fontName='PingFang', fontSize=size,
                          textColor=color, leading=leading or size*1.6)

def stars(n, color, size=11):
    filled = '★' * n
    empty  = '★' * (5 - n)
    parts  = (f'<font color="{color.hexval()}">{filled}</font>'
              f'<font color="#e8ddd2">{empty}</font>'
              f' <font color="#a08060" size="9">{n}/5</font>')
    return Paragraph(parts, ParagraphStyle('s', fontName='PingFang',
                                           fontSize=size, leading=size*1.5))

def badge(txt, bg=ORANGE):
    return Paragraph(
        f'<font color="#fff">{txt}</font>',
        ParagraphStyle('b', fontName='PingFang', fontSize=9, leading=13,
                       backColor=bg, borderPadding=(3,7,3,7))
    )

story = []

# Title
story.append(Paragraph("ATPI × 應用場景　重要性矩陣", ps(18, ORANGE, 28)))
story.append(Spacer(1, 2*mm))
story.append(Paragraph("各場景中 A吸引力 / T信任力 / P專業力 / I推進力 的關鍵程度（滿分 5 顆星）",
                        ps(10, MID, 16)))
story.append(Spacer(1, 5*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 5*mm))

# Header row
def hdr(txt, color=MID):
    return Paragraph(txt, ParagraphStyle('h', fontName='PingFang', fontSize=10,
                                         textColor=color, leading=14))

data = [
    [hdr("應用場景"), hdr("A 吸引力", ORANGE), hdr("T 信任力", TEAL),
     hdr("P 專業力", BLUE), hdr("I 推進力", GOLD), hdr("關鍵維度")],
]

rows = [
    ("短影音／社群內容", 5, 3, 3, 1, "A"),
    ("演講／舞台",       5, 1, 3, 5, "A + I"),
    ("1 對 1 銷售",     3, 5, 3, 5, "T + I"),
    ("1 對 N 課程招生", 5, 3, 4, 3, "A + P"),
    ("深度諮詢",         1, 5, 5, 3, "T + P"),
    ("轉介紹系統",       1, 5, 3, 3, "T"),
    ("募資／招商提案",   3, 3, 5, 5, "P + I"),
    ("談判／合作",       1, 5, 5, 3, "T + P"),
    ("企業培訓 B2B",    3, 3, 5, 5, "P + I"),
    ("社群直播",         5, 3, 3, 5, "A + I"),
]

# Pick badge color by key
KEY_COLORS = {
    "A": ORANGE, "T": TEAL, "P": BLUE, "I": GOLD,
    "A + I": colors.HexColor("#c05a30"),
    "T + I": colors.HexColor("#3a9a85"),
    "A + P": colors.HexColor("#7a6aaa"),
    "T + P": colors.HexColor("#2a7abf"),
    "P + I": colors.HexColor("#8a7a30"),
}

for scene, a, t, p, i, key in rows:
    bc = KEY_COLORS.get(key, ORANGE)
    data.append([
        Paragraph(scene, ps(10, DARK, 15)),
        stars(a, ORANGE),
        stars(t, TEAL),
        stars(p, BLUE),
        stars(i, GOLD),
        badge(key, bc),
    ])

col_w = [38*mm, 28*mm, 28*mm, 28*mm, 28*mm, 22*mm]

t = Table(data, colWidths=col_w, repeatRows=1)
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), LIGHT),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, colors.white]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (1,0), (4,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('RIGHTPADDING', (0,0), (-1,-1), 7),
]))
story.append(t)
story.append(Spacer(1, 8*mm))

# Legend
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("讀表邏輯", ps(12, ORANGE, 18)))
story.append(Spacer(1, 2*mm))
story.append(Paragraph(
    "你的 ATPI 最強的兩個維度 → 對應的場景就是你最容易變現的路徑。",
    ps(10, MID, 16)
))
story.append(Spacer(1, 3*mm))

examples = [
    ("A + T 強", "社群養粉 + 1 對 1 深聊成交"),
    ("A + I 強", "演講現場收單 + 社群直播帶貨"),
    ("T + P 強", "深度諮詢 + 談判合作"),
    ("P + I 強", "募資提案 + 企業培訓"),
]

ex_data = []
for combo, desc in examples:
    ex_data.append([
        Paragraph(combo, ps(10, ORANGE, 15)),
        Paragraph(desc,  ps(10, MID,    15)),
    ])

et = Table(ex_data, colWidths=[30*mm, 132*mm])
et.setStyle(TableStyle([
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [CREAM, colors.white]),
    ('BOX', (0,0), (-1,-1), 0.4, BORDER),
    ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(et)
story.append(Spacer(1, 8*mm))

# Footer
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 3*mm))
story.append(Paragraph("溝通變現能力教練　光頭", ps(9, BORDER, 14)))

doc.build(story)
print("PDF 已產出：", OUTPUT)
