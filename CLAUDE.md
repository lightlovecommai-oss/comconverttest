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

| 代碼 | 名稱 | 結果句 | 原版（填色） | 深版（文字） |
|------|------|------|------|------|
| A | 吸引肌肉 | 讓他想靠近 | #C6603A | #AF5433 |
| T | 信任肌肉 | 讓他願意說 | #6E8B77 | #5C7464 |
| P | 專業肌肉 | 讓他要找你 | #6E8CA8 | #54718D |
| I | 推進肌肉 | 讓他願意動 | #C99A4E | #8E682B |

✅ **2026-09-01 已對齊品牌正典**（真相＝productkit `1-手冊（內部）/21-品牌色彩系統.md`）。
本頁是暖底所以吃**暖版**；舊值（A#e8734a／T#5DCAA5／P#378ADD／I#c8a84b）是「科技霓虹版」＝深底專用，已作廢。
**規則一句話：填色與大字用原版，小字與小元件用深版**（`DIMS[k].color` vs `DIMS[k].textColor`）。
⚠️ I 原版 `#C99A4E` 連大字都不合格（2.28:1），**任何文字一律走 textColor**。

骨架＝**門檻級聯**：A 點火（0–10°）→ T 抬底線（10–50°）→ P 墊天花板（50–90°）→ I 閥門（90–100°）；任一塊趨近零時嚴重折損（`缺一即零` 已作廢）。

## 12 小肌群（基礎版的輸出單位）　🆕 2026-09-01
每維 3 題＝3 個小肌群，**題數不變（16 題）、輸出從 4 格變 12 格**。
定義（格名／技巧／週測問法）全部來自 `atpi-core.js` 的 `MUSCLES`，本專案不自己維護一份。

| A 吸引 | T 信任 | P 專業 | I 推進 |
|---|---|---|---|
| A1 讓他開口 | T1 讓他敢說 | P1 讓他釐清 | I1 讓他想要 |
| A2 讓他追問 | T2 讓他交心 | P2 讓他有感 | I2 讓他敢要 |
| A3 讓他記得 | T3 讓他當真 | P3 讓他放心 | I3 讓他答應 |

- 題幹＝把字典 12 格表的「一句話可觀察行為（週測問法）」改寫成情境選擇題，**問具體事例不問感覺**。
- 選項＝1–5 錨點（`ANCHORS`，即 `EVAL_ANCHORS` 拿掉「過頭訊號」那半句），
  所以**測驗分無縫就是健身房的體格分基線，不用換算**。
- 大肌肉分＝該維 3 小肌群平均 → 攤到 0–100（數值與舊版完全相同，換的是中介結構不是尺）。
- 🚫 **加強版 19 題**（最弱那維再細測 3 格）＝**付款完成後**才做，不是購買前；**完整版 28 題**＝私教學員專用。

## atpi-core.js（跨專案共用・不要直接改本 repo 這份）
ATPI 程式真相在 `../../4-溝通健身房/consult-workshop/atpi-core.js`，本 repo 放**同步副本**
（兩個 repo 各自獨立 GitHub Pages，沒辦法直接 `<script src>` 對方的檔案）。

```bash
./sync-atpi-core.sh          # 檢查有沒有跟真相檔漂掉
./sync-atpi-core.sh --write  # 從真相檔複製過來
```

它提供：`DORD` `MORD` `MUSCLES` `EVAL_ANCHORS` `dimFromMuscles` `weakestMuscles` `musclesOfDim`
`calcPotential` `getCombo` `STRONG_PATH` `COMBO_PATH` `WEAK_DESC` `drawRadarSVG`。
**`DIMS` 不在裡面**——它由各專案自己定義（本檔用暖版色盤），`drawRadarSVG` 會讀它。

## 頁面結構（五個 screen）
- `s-intro` — 首頁：應用場景卡片 → 測驗能幫你 → 學員故事 → 開始測驗
- `s-explain` — 測驗前說明：什麼是溝通變現 → 4 大肌肉逐塊說明 → 這個測驗會做什麼
- `s-quiz` — 答題頁：逐題顯示，含進度條
- `s-form` — 留資頁：姓名、Email、職業
- `s-result` — 結果頁：情境座標判讀（CTX）→ SVG 雷達圖 → **4 大肌肉 × 12 小肌群分數** → 強項組合變現路徑 → 最大缺口＋**最弱三塊小肌群** → 進館

## 結果頁重要元素
- 雷達圖：SVG 向量（非 canvas），實作在 `atpi-core.js` 的 `drawRadarSVG`，本檔只留 `drawRadar()` 薄包裝
- 分數欄位：雷達圖下方**單欄 4 張卡**，每張＝大肌肉名 + 分數 + 進度條 + **它的 3 個小肌群（1–5 五點燈）**
- 最弱三塊小肌群：`weakestMuscles(muscleScores,3)`，就是進館後的第一份課表

## 出口只有一個　🔴 2026-09-01 老師拍板「分流取消」
測完**全部進館**，不給第二個選項。已下架：
- ~~Calendly 諮詢鈕（btn-consult）~~
- ~~LINE 分享鈕（btn-share）＋ `shareQuiz()` ＋ `STRENGTH_INTRO`~~——分享卡的按鈕指回測驗本身，是迴圈不是出口

唯一出口＝`btn-workshop` →「進溝通健身房，開始練 →」，帶 `?id=<LINE userId>`。
⚠️ 免費路人也要進得去：`consult-workshop/index.html` 已改成
**在名單內但未開通 → `member.html`（會員模式）**，不再一律踢到 `showcase.html`。
名單那一列是測驗寫的（Code.gs `action:"quiz"` 會 `ensureRosterRow_`），
所以「不領取直接看結果」在拿得到 userId 時**也要送出**，否則進館會查無此人。

## 資料流（測完寫兩個地方）
```
測完 → POST action:"quiz"  → (漏斗)能力測驗  ：一人一列 upsert，含 Q1..Q12、情境座標五欄
     → POST action:"eval"  → (遊戲)體測紀錄  ：12 列小肌群 1–5，source="quiz" ＝體格分基線
```
- `postEvals()` 自己防重複送（`cct_eval_sent_v1` 存 userId＋分數 signature）——
  eval 端點是 **append 不是 upsert**，不擋的話每次重開結果頁都會多疊 12 列假紀錄。
- **Q1..Q12 ＝ A1..I3 的 1–5 原始分**（照 `MORD` 順序）。
  ⚠️ 2026-09-01 以前的舊列 Q 欄是別的意思（Q1 其實是 GOAL 題、尾巴還被截掉），**新舊列不可混著比**。

## 重要變數（JS）
- `QS` — 題目陣列（16 題；**12 題各帶一個 `muscle` 欄**＝A1..I3，GOAL/CTX/SRC/INC 不計分）
- `ANCHORS` — 1–5 錨點選項（＝`EVAL_ANCHORS` 的精簡版）
- `muscleScores` — **12 小肌群 1–5 原始分**，本次改版的中介層；`scores` 由它平均出來，體格基線也是它
- `DIMS` — 4 大肌肉定義（name / desc / **color 原版 / textColor 深版**）
- `CTX_OPTS` — 情境座標（G4）：不進計分，只判讀「這組分數是對誰的分數」，`key` ＝這種對象最先卡住的那塊肌肉
- `CTA_DESC` — 結果頁出口文案（依最弱那塊大肌肉；2026-09-01 起導向進館，不再導 Calendly）
- `STRONG_DESC` — 各塊肌肉改進建議（⚠️ 目前沒有任何地方讀它，留著待用）
- `INC_TITLES / INC_BEAT / INC_NEXT` — 收入等級對應文字（⚠️ 同上，目前未使用）
- `LIFF_ID` — LINE LIFF ID
- `SHEET_API` — Google Apps Script API URL

## Git 工作流程
```bash
# 改完後直接 commit + push
git add index.html atpi-core.js sync-atpi-core.sh CLAUDE.md
git commit -m "說明"
git push origin main
# GitHub Pages 約 1-2 分鐘後更新
```

## 開發預覽
- launch.json 已設定 python3 http.server port 3000
- 跳到結果頁測試用（⚠️ 現在一定要餵 `muscleScores`，結果頁整頁靠 12 格畫）：
```js
muscleScores={A1:4,A2:2,A3:3, T1:4,T2:5,T3:4, P1:3,P2:1,P3:2, I1:3,I2:2,I3:4};
DORD.forEach(k=>scores[k]=Math.round(dimFromMuscles(muscleScores)[k]/5*100));
scores.potential=calcPotential(scores).unlocked;
incIdx=1; goalIdx=2; srcIdx=0; ctxIdx=4;
renderResult(); setTimeout(drawRadar, 200);
```
- ⚠️ **測試時不要設 `userId`**：`btn-skip` / `btn-rep` 會真的 POST 到正式試算表。
  要驗證送出內容就攔 `window.fetch`，別讓它真的打出去。
