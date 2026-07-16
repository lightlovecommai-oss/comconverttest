from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Chinese font
pdfmetrics.registerFont(TTFont('PingFang', '/Library/Fonts/Arial Unicode.ttf'))

W, H = A4
OUTPUT = "/Users/ivor/comconvertai/comconverttest/BNI商業策略資料.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=18*mm, bottomMargin=18*mm
)

# Colors
ORANGE = colors.HexColor("#e8734a")
DARK   = colors.HexColor("#2d1f0f")
MID    = colors.HexColor("#6b4c30")
LIGHT  = colors.HexColor("#f5ede3")
CREAM  = colors.HexColor("#fdf8f3")
BORDER = colors.HexColor("#e8ddd2")
GOLD   = colors.HexColor("#c8a84b")

def style(size=11, color=DARK, bold=False, leading=None):
    return ParagraphStyle(
        'custom',
        fontName='PingFang',
        fontSize=size,
        textColor=color,
        leading=leading or size*1.6,
        spaceAfter=0,
    )

story = []

# ── Title ──
story.append(Paragraph("BNI 商業策略資料", ParagraphStyle(
    'title', fontName='PingFang', fontSize=20, textColor=ORANGE,
    leading=30, spaceAfter=4
)))
story.append(Paragraph("光頭 · 溝通變現能力教練", style(11, MID)))
story.append(Spacer(1, 6*mm))
story.append(HRFlowable(width="100%", thickness=1, color=BORDER))
story.append(Spacer(1, 6*mm))

# ══════════════════════════════
# 第一點
# ══════════════════════════════
story.append(Paragraph("第一點　手上的客戶資源", style(15, ORANGE)))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(
    "我的客戶主要是<b>有專業、想提升收入的個人工作者</b>，集中在身心靈、幸福學、財商圈子，"
    "年營業額 50–2000 萬之間。他們通常也需要：個人品牌包裝、形象攝影、財務規劃、網站建置。"
    "如果你服務的客戶是這類人，我們可以互相介紹。",
    ParagraphStyle('body', fontName='PingFang', fontSize=10.5, textColor=MID,
                   leading=18, spaceAfter=0)
))
story.append(Spacer(1, 4*mm))

# Client table
client_data = [
    ["排名", "人名", "產業", "痛點", "年營業額（萬）"],
    ["1",  "小紀",    "幸福學老師",   "流量放大",    "1000–2000"],
    ["2",  "路隊長",  "Podcaster",    "不同產品變現", "800"],
    ["3",  "Lily老師","幸福學老師",   "流量放大",    "200"],
    ["4",  "塔塔",    "財商老師",     "流量放大",    "200"],
    ["5",  "Cindy",   "財商老師",     "商業模式",    "200"],
    ["6",  "雅雯",    "脈輪舞蹈",     "商業模式",    "150"],
    ["7",  "Nora",    "幸福學顧問",   "沒產品",      "100"],
    ["8",  "珈鉉",    "希塔療癒",     "商業模式",    "100"],
    ["9",  "Vicky",   "身心靈",       "商業模式",    "100"],
    ["10", "豐翔哥",  "種子法則",     "開始起步",    "100"],
    ["11", "NANA",    "服裝穿搭",     "開始起步",    "50"],
    ["12", "Cynthia", "醫美診所",     "商業模式",    "50"],
    ["—",  "Ken哥",   "媒體出版業",   "—",           "—"],
    ["—",  "春美",    "房仲",         "開始起步",    "—"],
    ["—",  "angelyn", "家族排列",     "開始起步",    "—"],
    ["—",  "黛比",    "情緒溝通",     "商業模式",    "—"],
    ["—",  "VK 米雪兒","直銷",        "商業模式",    "—"],
]

col_w = [12*mm, 22*mm, 38*mm, 38*mm, 32*mm]

def cell(txt, bold=False, color=DARK, size=9.5, align='LEFT'):
    s = ParagraphStyle('c', fontName='PingFang', fontSize=size,
                       textColor=color, leading=size*1.5)
    return Paragraph(str(txt), s)

table_data = []
for r_i, row in enumerate(client_data):
    bold = (r_i == 0)
    col = ORANGE if bold else DARK
    table_data.append([cell(v, bold=bold, color=col, size=9 if bold else 9.5) for v in row])

t = Table(table_data, colWidths=col_w, repeatRows=1)
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), LIGHT),
    ('BACKGROUND', (0,1), (-1,-1), CREAM),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, colors.white]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('ROUNDEDCORNERS', [4]),
]))
story.append(t)
story.append(Spacer(1, 8*mm))

# ══════════════════════════════
# 第二點
# ══════════════════════════════
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 5*mm))
story.append(Paragraph("第二點　我想要的人脈引薦", style(15, ORANGE)))
story.append(Spacer(1, 3*mm))

story.append(Paragraph(
    "<b>一句話版本：</b>「我在找有專業、有在做、但收入卡關的人——"
    "特別是年收 60–120 萬這段，覺得客戶不夠多、成交率不夠高、"
    "或是不知道怎麼漲價的。」",
    ParagraphStyle('quote', fontName='PingFang', fontSize=10.5, textColor=MID,
                   leading=18, leftIndent=8, borderPad=8,
                   borderColor=ORANGE, borderWidth=0)
))
story.append(Spacer(1, 4*mm))

# Three types
type_data = [
    ["① 講師／教練／顧問（最精準）",
     "身心靈老師、健身教練、心理諮商師、職涯教練、財務顧問\n"
     "痛點：有專業但招生難、學員不買單、不知道怎麼漲價\n"
     "期待：成交率提升、學生更多、漲價不怕"],
    ["② 業務／銷售人員（量大）",
     "保險、房仲、理財專員、B2B 業務\n"
     "痛點：說了很多但對方說「再考慮」，轉換率低\n"
     "期待：縮短成交周期、提升單子成功率"],
    ["③ 創業者／自由工作者（成長最快）",
     "設計師、攝影師、文案、行銷顧問\n"
     "痛點：接案靠人情、客戶砍價、不知道怎麼讓人主動找上門\n"
     "期待：讓客戶主動找上門、客單價提升"],
]

for title, body in type_data:
    row_data = [[
        Paragraph(title, ParagraphStyle('th', fontName='PingFang', fontSize=10,
                                        textColor=ORANGE, leading=16)),
        Paragraph(body.replace('\n','<br/>'),
                  ParagraphStyle('tb', fontName='PingFang', fontSize=9.5,
                                 textColor=MID, leading=16))
    ]]
    rt = Table(row_data, colWidths=[52*mm, 110*mm])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM),
        ('BOX', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(rt)
    story.append(Spacer(1, 2*mm))

story.append(Spacer(1, 2*mm))
story.append(Paragraph(
    "★ 甜蜜收入段：年收 60–120 萬——已經在做、有痛感、有意願改變",
    ParagraphStyle('note', fontName='PingFang', fontSize=10, textColor=GOLD, leading=16)
))
story.append(Spacer(1, 8*mm))

# ══════════════════════════════
# 第三點
# ══════════════════════════════
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 5*mm))
story.append(Paragraph("第三點　我想被帶來賓的產業別", style(15, ORANGE)))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(
    "我最希望認識這五類人，因為我們服務的是同一批客戶，可以長期互相轉介紹。",
    ParagraphStyle('body2', fontName='PingFang', fontSize=10.5, textColor=MID, leading=18)
))
story.append(Spacer(1, 4*mm))

industry_data = [
    ["優先", "產業", "轉介紹理由"],
    ["★★★", "個人品牌攝影師",
     "客戶跟你 TA 幾乎一樣。照片拍好了，下一步是讓對方看了之後願意掏錢。"],
    ["★★★", "形象顧問／穿搭顧問",
     "TA 100% 重疊——想在職場或商場上更有影響力的人。"],
    ["★★★", "商業教練／創業顧問",
     "同一個客戶的不同層面：他做策略，你做溝通和成交。天然互補。"],
    ["★★",  "保險業務（企業主型）",
     "大量接觸你的 TA，客戶剛好在 60–120 萬這個收入段。"],
    ["★★",  "記帳士／會計師",
     "服務自由工作者和小老闆，正是你的甜蜜客群。"],
]

ind_col_w = [14*mm, 42*mm, 106*mm]

ind_table = []
for r_i, row in enumerate(industry_data):
    bold = (r_i == 0)
    color = ORANGE if bold else DARK
    if r_i == 0:
        ind_table.append([cell(v, color=ORANGE, size=9) for v in row])
    else:
        star_color = GOLD if row[0].startswith("★★★") else MID
        ind_table.append([
            cell(row[0], color=star_color, size=9.5),
            cell(row[1], color=DARK, size=9.5),
            cell(row[2], color=MID, size=9.5),
        ])

it = Table(ind_table, colWidths=ind_col_w, repeatRows=1)
it.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), LIGHT),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, colors.white]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(it)
story.append(Spacer(1, 10*mm))

# Footer
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(
    "溝通變現能力教練　光頭",
    ParagraphStyle('footer', fontName='PingFang', fontSize=9, textColor=BORDER, leading=14)
))

doc.build(story)
print("PDF 已產出：", OUTPUT)
