# comconverttest — 溝通變現能力測驗

> ↔ **企劃大腦**：本專案是產品「ATPI 測驗（引流品）」的執行。產品定義／商業模式見 `../../5-企劃與產品手冊/productkit`（核心概念真相＝`1-手冊（內部）/01-核心定義字典.md`）。

## 專案概覽
單一 HTML 檔案的 LINE LIFF 測驗問卷，評估用戶的「溝通變現能力」並收集潛在客戶資料。
- **線上網址**：https://lightlovecommai-oss.github.io/comconverttest/
- **Repo**：https://github.com/lightlovecommai-oss/comconverttest
- **技術**：純 HTML + CSS + 原生 JS，無框架，整合 LINE LIFF SDK + Google Apps Script

## 教學三大應用場景
1. **日常溝通** — 與同事、家人、朋友溝通取得共鳴，讓老闆主動賞識、關係和諧、說話有份量
2. **1 對 1 銷售** — 吸引而非推銷，讓對方主動詢問更多、自己說服自己成交
3. **1 對 N 演講／課程** — 感召式演講，吸引台下而非強推，讓每個人覺得「這說的就是我」

## 4 大肌肉（ATPI）
> 用詞正典：四塊一律叫「〇〇肌肉」，`〇〇力／四力／四維／四大肌群` 皆已作廢；集合詞用「4 大肌肉／12 小肌群」。

| 代碼 | 名稱 | 定義 | 顏色（本專案現值） |
|------|------|------|------|
| A | 吸引肌肉 | 讓人想靠近你 | #e8734a |
| T | 信任肌肉 | 讓人願意相信你 | #5DCAA5 |
| P | 專業肌肉 | 讓人覺得你很會 | #378ADD |
| I | 推進肌肉 | 讓人願意行動 | #c8a84b |

⚠️ 品牌正典的 ATPI 四色是 A #e8734a / T #33c495 / P #4b9bf0 / I #e6a93a，本檔 T/P/I 三色與正典不同（雷達圖、分數卡、LINE 分享卡都吃這組值）——要不要對齊待老師拍板。

骨架＝**門檻級聯**：A 點火（0–10°）→ T 抬底線（10–50°）→ P 墊天花板（50–90°）→ I 閥門（90–100°）；任一塊趨近零時嚴重折損（`缺一即零` 已作廢）。

## 頁面結構（五個 screen）
- `s-intro` — 首頁：應用場景卡片 → 測驗能幫你 → 學員故事 → 開始測驗
- `s-explain` — 測驗前說明：什麼是溝通變現 → 4 大肌肉逐塊說明 → 這個測驗會做什麼
- `s-quiz` — 答題頁：逐題顯示，含進度條
- `s-form` — 留資頁：姓名、Email、職業
- `s-result` — 結果頁：情境座標判讀（CTX）→ SVG 雷達圖 → 四塊肌肉分數 → 強項組合變現路徑 → 最大缺口 → 按鈕

## 結果頁重要元素
- 雷達圖：SVG 向量（非 canvas），點擊各塊肌肉的 dot 顯示 tooltip 分數
- 分數欄位：雷達圖下方 2×2 grid，各塊肌肉顏色 + 大數字 + 進度條
- 諮詢按鈕文字：「預約「提升溝通變現」諮詢」
- 分享 LINE 卡片：顯示強項肌肉名稱 + 尚未解鎖潛力 + STRENGTH_INTRO 說明

## 重要變數（JS）
- `QS` — 題目陣列（16 題；A/T/P/I 各 3 題計分，GOAL/CTX/SRC/INC 不計分）
- `DIMS` — 4 大肌肉定義（name / desc / color）
- `CTX_OPTS` — 情境座標（G4）：不進計分，只判讀「這組分數是對誰的分數」，`key` ＝這種對象最先卡住的那塊肌肉
- `STRENGTH_INTRO` — 各塊肌肉強項說明（分享卡片用）
- `STRONG_DESC` — 各塊肌肉改進建議
- `INC_TITLES / INC_BEAT / INC_NEXT` — 收入等級對應文字
- `LIFF_ID` — LINE LIFF ID
- `SHEET_API` — Google Apps Script API URL

## Git 工作流程
```bash
# 改完後直接 commit + push
git add index.html
git commit -m "說明"
git push origin main
# GitHub Pages 約 1-2 分鐘後更新
```

## 開發預覽
- launch.json 已設定 python3 http.server port 3000
- 跳到結果頁測試用：
```js
window.scores={A:78,T:62,P:85,I:55};
window.incIdx=2; window.goalIdx=3;
window.ans=[2,3,2,3,2,3,2,3,2,1,2,2];
renderResult(); setTimeout(drawRadar, 200);
```
