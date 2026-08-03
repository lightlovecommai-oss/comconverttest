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

## 四個評分維度（ATPI）
| 代碼 | 名稱 | 定義 | 顏色 |
|------|------|------|------|
| A | 吸引力 | 讓人想靠近你 | #e8734a |
| T | 信任力 | 讓人願意相信你 | #5DCAA5 |
| P | 專業力 | 讓人覺得你很會 | #378ADD |
| I | 影響力 | 讓人願意行動 | #c8a84b |

## 頁面結構（四個 screen）
- `s-intro` — 首頁：應用場景卡片 → 測驗能幫你 → 學員故事 → 開始測驗
- `s-quiz` — 答題頁：逐題顯示，含進度條
- `s-form` — 留資頁：姓名、Email、職業
- `s-result` — 結果頁：主/副能力 → 擊敗百分比卡片 → SVG 雷達圖 → 四欄分數 → 建議 → 按鈕

## 結果頁重要元素
- 雷達圖：SVG 向量（非 canvas），點擊各維度 dot 顯示 tooltip 分數
- 分數欄位：雷達圖下方 2×2 grid，各維度顏色 + 大數字 + 進度條
- 諮詢按鈕文字：「預約「提升溝通變現」諮詢」
- 分享 LINE 卡片：顯示主能力名稱 + 擊敗百分比 + STRENGTH_INTRO 說明

## 重要變數（JS）
- `QS` — 題目陣列（13 題）
- `DIMS` — 四維度定義
- `STRENGTH_INTRO` — 各維度強項說明（分享卡片用）
- `STRONG_DESC` — 各維度改進建議
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
