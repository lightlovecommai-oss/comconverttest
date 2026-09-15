#!/usr/bin/env python3
"""把正式 index.html 的每個畫面抓成「左邊看畫面、右邊寫修改」的可改版 demo。

用法：python3 _build-quiz-demo.py   →  寫出 demo-quiz-all.html

⚠️ 這支不手抄畫面。它用 headless Chrome 真的跑一次 index.html，把每個狀態的真 DOM
   （含 renderQ／renderResult／renderMuscleMap 產生出來的東西）dump 下來再包裝。
   舊版 demo-quiz-all.html 是手抄的，index 一改就漂掉、對不上——所以改成產生器：
   **index.html 改了就重跑這支，不要動 demo 的畫面內容。**
"""
import html as _html
import json
import re
import subprocess
import sys
from hashlib import md5
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "index.html"
OUT = HERE / "demo-quiz-all.html"
TMP = HERE / "_cap.tmp.html"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SHELL_VER = "s2"   # 改了外殼（尤其是 SKIP／編號規則）就 +1，草稿的 localStorage key 才會跟著換

# ── 每屏的標題與說明（唯一維護處；畫面內容一律從 index.html 抓） ──────────────
META = {
    "boot":    ("畫面 0｜開場等待頁（boot）",
                "開頁先蓋滿版咖啡漸層卡，LIFF 載入完成就收掉。跨頁 canon：載入中一律咖啡漸層。"),
    "tb":      ("共用｜席位橫幅",
                "每個畫面上方都有。quiz＝A 磚橘席位色；連點 logo 5 下＝重測彩蛋；Aa＝字級開關。"),
    "intro":   ("畫面 1｜首頁（s-intro）",
                "好奇鉤子 → 這份測驗為誰做 → 影響力之路 → 開始測驗。"),
    "explain": ("畫面 2｜測驗前說明（s-explain）",
                "四塊肌肉各一行，講清楚等一下在量什麼。"),
    "form":    ("畫面 4｜留資頁（s-form）",
                "測完才留資（先給價值再要資料）。可以不領取直接看結果。"),
    "result":  ("畫面 5｜結果頁（s-result）",
                "分數＝示意樣本，走的是正式公式（atpi-core.js）。MUSCLE MAP 這裡是收合態。"),
    "mapopen": ("畫面 5b｜MUSCLE MAP 展開",
                "12 小塊：形狀是真的、分數糊掉＝進館才全開。這是 quiz 最大的鉤子。"),
    "tie":     ("畫面 5c｜結果頁・平手版（同一張卡的另一種狀態）",
                "上面那張是「三塊分數分得開」的樣子。這張是同分時的樣子：不編號、不硬排名次，"
                "兩塊都掛「進館可選」，讓他自己挑。一題 1–5 整數，同分是常態不是例外。"),
}

# ── 1. 造一支會自己把每屏 DOM 吐出來的臨時檔 ─────────────────────────────────
HARNESS = r"""
<script>
window.addEventListener("load", function(){ setTimeout(function(){
  var out = [];
  function grab(key, sel, outer){
    var el = document.querySelector(sel);
    /* outer＝連自己的 class 一起帶走（席位橫幅的漸層底就掛在 .tb 自己身上） */
    out.push({ key:key, html: el ? (outer ? el.outerHTML : el.innerHTML) : "(找不到 " + sel + ")", extra:{} });
  }
  try {
    grab("boot", "#boot");
    grab("tb", "#app-logo", true);
    grab("intro", "#s-intro .wrap");
    grab("explain", "#s-explain .wrap");

    /* 16 題逐題：cur 往前走、前面的題目填上答案，進度條才是真的。
       第 3 題順便示範「選中」長什麼樣，其餘維持未選。 */
    show("s-quiz");
    ans = [];
    for (var i = 0; i < QS.length; i++) {
      cur = i;
      if (i === 2) ans[i] = 3;
      renderQ();
      out.push({ key:"q" + (i+1), html: document.querySelector("#s-quiz .wrap").innerHTML,
                 extra: { label: QS[i].label || "", muscle: QS[i].muscle || "" } });
      if (ans[i] === undefined) ans[i] = 2;
    }

    grab("form", "#s-form .wrap");

    /* 結果頁示意樣本：給 12 小肌群 1–5 的原始分，其餘一律走正式公式算出來，
       不要手填 scores——手填就會跟公式漂掉。 */
    var SAMPLE = { A:3, T:4, P:2, I:3 };
    muscleScores = {};
    DORD.forEach(function(k){
      musclesOfDim(k).forEach(function(m, idx){
        muscleScores[m] = Math.min(5, Math.max(1, SAMPLE[k] + (idx === 1 ? 1 : (idx === 2 ? -1 : 0))));
      });
    });
    var dim = dimFromMuscles(muscleScores);
    DORD.forEach(function(k){ scores[k] = pctFromEval(dim[k]); });
    scores.potential = calcPotential(scores).unlocked;
    incIdx = 1; goalIdx = 2; srcIdx = 0; ctxIdx = 1;
    show("s-result");
    renderResult();
    drawRadar();   /* renderResult 是 setTimeout 100ms 才畫雷達，這裡不補就抓到空的 <svg> */
    out.push({ key:"result", html: document.querySelector("#s-result .wrap").innerHTML, extra:{} });

    toggleMuscleMap();
    out.push({ key:"mapopen", html: document.getElementById("bs-map").closest(".dq-blk").outerHTML, extra:{} });

    /* 平手版：示意樣本剛好三塊分得開，所以看不到平手的樣子。
       這裡把最弱那維的其中兩塊壓成同分再 render 一次，只抓那張卡。 */
    var wkDim = getCombo(scores).wk;
    var wm = musclesOfDim(wkDim).slice().sort(function(a,b){ return muscleScores[a] - muscleScores[b]; });
    /* 做成「兩塊平手、第三塊分得開」＝最常見的樣子。三塊全平會看不到並列與未解鎖同時出現。 */
    muscleScores[wm[1]] = muscleScores[wm[0]];
    if (muscleScores[wm[2]] - muscleScores[wm[0]] < 1) muscleScores[wm[2]] = Math.min(5, muscleScores[wm[0]] + 2);
    renderResult();
    drawRadar();
    out.push({ key:"tie", html: document.getElementById("r-weak3").closest(".card").outerHTML, extra:{} });
  } catch (e) {
    out.push({ key:"__error", html: String(e && e.stack || e), extra:{} });
  }
  var s = document.createElement("script");
  s.id = "CAPDATA"; s.type = "application/json";
  s.textContent = JSON.stringify(out).replace(/</g, "\\u003c");
  document.body.appendChild(s);
}, 400); });
</script>
"""


def capture():
    src = SRC.read_text(encoding="utf-8")
    TMP.write_text(src.replace("</body>", HARNESS + "\n</body>"), encoding="utf-8")
    try:
        dom = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=12000",
             "--dump-dom", "file://" + str(TMP.resolve())],
            capture_output=True, text=True, timeout=120,
        ).stdout
    finally:
        TMP.unlink(missing_ok=True)
    m = re.search(r'<script id="CAPDATA"[^>]*>(.*?)</script>', dom, re.S)
    if not m:
        sys.exit("抓不到 CAPDATA——index.html 可能在 load 前就丟例外了，先用瀏覽器開一次看 console。")
    boards = json.loads(_html.unescape(m.group(1)))
    bad = [b for b in boards if b["key"] == "__error"]
    if bad:
        sys.exit("harness 在頁內丟例外：\n" + bad[0]["html"])
    return boards


def inert(html_, key):
    """把抓下來的 DOM 去活化：拔掉 onclick（demo 裡按下去只會噴錯），
    id 加屏別前綴（16 題各帶一份 q-counter，不加前綴整份文件會有一堆重複 id）。"""
    html_ = re.sub(r'\son[a-z]+="[^"]*"', "", html_)
    # 連結收成 data-href：要改連結上的字就得能點進去而不被帶走頁面
    html_ = re.sub(r'\shref="(?!#)([^"]*)"', r' data-href="\1"', html_)
    return re.sub(r'\bid="([^"]+)"', lambda m: 'id="%s__%s"' % (key, m.group(1)), html_)


def build():
    boards = capture()
    css = re.search(r"<style>(.*?)</style>", SRC.read_text(encoding="utf-8"), re.S).group(1)

    sections = []
    for b in boards:
        key = b["key"]
        if key.startswith("q"):
            n = key[1:]
            title = "畫面 3-%s｜第 %s 題（共 %d 題）" % (n, n, sum(1 for x in boards if x["key"].startswith("q")))
            sub = b["extra"].get("label", "")
            if b["extra"].get("muscle"):
                sub += "・肌肉題（1–5 錨點，選了就自動前進）"
            else:
                sub += "・不計分"
        else:
            title, sub = META.get(key, (key, ""))
        sections.append(
            '<section class="x-row" data-key="%s">'
            '<div class="x-left">'
            '<div class="x-cap"><b>%s</b><span>%s</span></div>'
            '<div class="x-frame%s" data-key="%s">%s</div>'
            '</div>'
            '<aside class="x-side">'
            '<div class="x-sh">在這裡寫你要怎麼改</div>'
            '<textarea class="x-note" data-key="%s" '
            'placeholder="這一屏想改什麼？直接寫（自動存）"></textarea>'
            '<div class="x-diff" data-key="%s"></div>'
            '</aside>'
            '</section>'
            % (key, _html.escape(title), _html.escape(sub),
               " x-dark" if key == "boot" else "", key, inert(b["html"], key), key, key)
        )

    body = "\n".join(sections)
    # 版本＝畫面內容＋外殼版本。外殼改了 data-edit 的編號規則也會位移，所以兩個都要進 hash。
    ver = md5((SHELL_VER + "".join(b["key"] + b["html"] for b in boards)).encode()).hexdigest()[:8]

    page = PAGE.replace("__CSS__", css).replace("__BODY__", body).replace("__VER__", ver)
    OUT.write_text(page, encoding="utf-8")
    print("寫出 %s" % OUT.name)
    print("  %d 屏、%d KB、版本 %s" % (len(boards), round(len(page) / 1024), ver))


PAGE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>quiz 可改版 demo・左看畫面右寫修改</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700;900&display=swap">
<style>
/* ══ 這一段是正式 index.html 的 CSS 原封不動搬過來（由 _build-quiz-demo.py 注入） ══
   別在這裡改樣式——改了下次重跑產生器就沒了。要改樣式請改 index.html。 */
__CSS__
</style>
<style>
/* ══ demo 外殼（全部 x- 開頭，跟正式頁的 class 不會撞） ══ */
html,body{background:#1b1512;color:#EFE6DE;font-family:"Noto Sans TC","PingFang TC",-apple-system,sans-serif;margin:0;}
#x-bar{position:sticky;top:0;z-index:900;display:flex;align-items:center;gap:14px;flex-wrap:wrap;
       background:#241b17;border-bottom:1px solid #3a2c25;padding:11px 18px;}
#x-bar h1{font-size:15px;font-weight:700;margin:0;letter-spacing:.04em;color:#EFE6DE;}
#x-bar .x-sp{flex:1;}
#x-bar .x-tip{font-size:12.5px;color:#9b8478;}
#x-cnt{font-size:13px;color:#C99A4E;font-weight:700;}
#x-bar button{font-family:inherit;font-size:13.5px;font-weight:600;border:0;border-radius:9px;
              padding:9px 15px;cursor:pointer;background:#C6603A;color:#fff;}
#x-bar button.x-ghost{background:transparent;color:#C9B6A8;border:1px solid #4a382f;}
#x-bar button:disabled{opacity:.4;cursor:default;}
#x-toc{display:flex;gap:7px;flex-wrap:wrap;padding:12px 18px 4px;}
#x-toc a{font-size:12px;color:#C9B6A8;background:#2f2420;border:1px solid #3f312a;
         border-radius:20px;padding:4px 11px;text-decoration:none;}
#x-toc a:hover{border-color:#C6603A;color:#FFD79A;}

.x-row{display:flex;gap:22px;align-items:flex-start;padding:26px 18px;border-top:1px solid #2b211c;}
.x-left{flex:0 0 400px;}
.x-cap{padding:0 2px 10px;}
.x-cap b{display:block;font-size:14.5px;color:#EFE6DE;}
.x-cap span{display:block;font-size:12px;color:#8a7266;margin-top:4px;line-height:1.6;}
.x-frame{width:400px;background:#F7F1EC;color:#4A1B0C;border-radius:10px;padding:14px 12px;
         box-shadow:0 10px 34px rgba(0,0,0,.45);overflow:hidden;}
.x-frame.x-dark{background:#F7F1EC;}
.x-frame,.x-frame *{font-family:"Noto Sans TC","PingFang TC",-apple-system,sans-serif;}
.x-frame .screen{display:block;}
.x-frame .wrap{max-width:none;padding:0;}

.x-side{flex:1;min-width:260px;position:sticky;top:64px;}
.x-sh{font-size:12px;color:#8a7266;letter-spacing:.06em;margin-bottom:7px;}
.x-note{width:100%;min-height:120px;resize:vertical;background:#FFF6D8;border:1.5px dashed #D9BE6A;
        border-radius:10px;padding:11px 13px;font-family:inherit;font-size:14px;line-height:1.75;
        color:#5A4A1E;outline:none;}
.x-note:focus{border-color:#C99A4E;border-style:solid;}
.x-diff{margin-top:11px;}
.x-diff .x-d{background:#2f2420;border:1px solid #3f312a;border-radius:9px;padding:9px 11px;margin-bottom:8px;}
.x-diff .x-o{font-size:12.5px;color:#9b8478;text-decoration:line-through;line-height:1.65;}
.x-diff .x-n{font-size:13px;color:#FFD79A;line-height:1.7;margin-top:4px;}

/* 直接改字：只有「自己身上就有文字」的元素可編輯，結構不會被改壞 */
[data-edit]{outline:1px dashed transparent;border-radius:3px;transition:outline-color .12s,background .12s;}
body.x-marks [data-edit]{outline-color:rgba(198,96,58,.38);}
[data-edit]:hover{outline-color:rgba(198,96,58,.85);background:rgba(198,96,58,.07);}
[data-edit]:focus{outline:2px solid #C6603A;background:#fff;}
[data-edit].x-dirty{background:#FFF6D9;outline-color:#C99A4E;}
/* 選取用淡琥珀底＋深墨字，不用系統反白（會蓋掉字，看不到自己改了什麼） */
[data-edit]::selection,[data-edit] *::selection{background:#FFD79A;color:#4A1B0C;}

@media (max-width:900px){ .x-row{flex-direction:column;} .x-left{flex:none;} .x-side{position:static;width:100%;} }
</style>
</head>
<body class="x-marks">

<div id="x-bar">
  <h1>quiz 可改版 demo</h1>
  <span class="x-tip">左邊畫面上點任何一段字就能直接改；右邊寫你的想法。都會自動存。</span>
  <span class="x-sp"></span>
  <span id="x-cnt">尚未修改</span>
  <button class="x-ghost" id="x-toggle">隱藏虛線</button>
  <button class="x-ghost" id="x-reset">清空全部</button>
  <button id="x-copy" disabled>複製全部修改</button>
</div>
<div id="x-toc"></div>

__BODY__

<script>
/* 版本號綁畫面內容（__VER__）：index.html 一改、重跑產生器，key 就換，
   舊草稿不會蓋在對不上的新畫面上。 */
var LSKEY = "cctdemo___VER__";
/* BUTTON 不排除——CTA 的字最需要改。抓下來的 DOM 已由產生器拔掉 onclick，點下去不會亂跑。 */
var SKIP = new Set(["SCRIPT","STYLE","SVG","PATH","CIRCLE","LINE","POLYGON","INPUT","TEXTAREA","BR","OPTION","SELECT"]);
var store = [];

document.querySelectorAll(".x-frame").forEach(function(frame){
  var key = frame.dataset.key, n = 0;
  frame.querySelectorAll("*").forEach(function(el){
    if (SKIP.has(el.tagName.toUpperCase())) return;
    if (el.closest("svg")) return;
    var own = [].some.call(el.childNodes, function(c){ return c.nodeType === 3 && c.textContent.trim(); });
    if (!own) return;
    /* 巢狀的不再標一次：外層已可編輯，內層再標會讓瀏覽器整塊反白蓋住字 */
    if (el.parentElement && el.parentElement.closest("[data-edit]")) return;
    var id = key + ":" + (n++);
    el.setAttribute("data-edit", id);
    el.setAttribute("contenteditable", "true");
    el.spellcheck = false;
    store.push({ id:id, key:key, el:el, original:el.innerText.trim() });
  });
});

var byId = {}; store.forEach(function(s){ byId[s.id] = s; });
var notes = [].slice.call(document.querySelectorAll(".x-note"));
var cntEl = document.getElementById("x-cnt"), copyBtn = document.getElementById("x-copy");

/* 貼上一律轉純文字，免得把 Word／網頁樣式帶進來 */
document.addEventListener("paste", function(e){
  var host = e.target.closest && e.target.closest("[data-edit]");
  if (!host) return;
  e.preventDefault();
  document.execCommand("insertText", false, e.clipboardData.getData("text/plain"));
});

function load(){
  var d = {};
  try { d = JSON.parse(localStorage.getItem(LSKEY) || "{}"); } catch (e) {}
  store.forEach(function(s){ if (d.edits && d.edits[s.id] !== undefined) s.el.innerText = d.edits[s.id]; });
  notes.forEach(function(t){ if (d.notes && d.notes[t.dataset.key]) t.value = d.notes[t.dataset.key]; });
}
function save(){
  var d = { edits:{}, notes:{} };
  store.forEach(function(s){ var v = s.el.innerText.trim(); if (v !== s.original) d.edits[s.id] = v; });
  notes.forEach(function(t){ if (t.value.trim()) d.notes[t.dataset.key] = t.value.trim(); });
  try { localStorage.setItem(LSKEY, JSON.stringify(d)); } catch (e) {}
}

function esc(t){ return t.replace(/&/g,"&amp;").replace(/</g,"&lt;"); }
function refresh(){
  var byKey = {};
  var n = 0;
  store.forEach(function(s){
    var now = s.el.innerText.trim(), ch = now !== s.original;
    s.el.classList.toggle("x-dirty", ch);
    if (ch) { n++; (byKey[s.key] = byKey[s.key] || []).push(s); }
  });
  document.querySelectorAll(".x-diff").forEach(function(box){
    var list = byKey[box.dataset.key] || [];
    box.innerHTML = list.map(function(s){
      return '<div class="x-d"><div class="x-o">' + esc(s.original)
           + '</div><div class="x-n">' + esc(s.el.innerText.trim()) + "</div></div>";
    }).join("");
  });
  var noted = notes.filter(function(t){ return t.value.trim(); }).length;
  cntEl.textContent = (n || noted) ? ("已改 " + n + " 處字・" + noted + " 則註記") : "尚未修改";
  copyBtn.disabled = !(n || noted);
  save();
}

/* 匯出＝直接進剪貼簿的純文字，這樣可以貼回對話，不用再傳檔案 */
function report(){
  var lines = ["# quiz demo 修改（版本 __VER__）"];
  document.querySelectorAll(".x-row").forEach(function(row){
    var key = row.dataset.key;
    var title = row.querySelector(".x-cap b").textContent;
    var note = row.querySelector(".x-note").value.trim();
    var eds = store.filter(function(s){ return s.key === key && s.el.innerText.trim() !== s.original; });
    if (!note && !eds.length) return;
    lines.push("", "## " + title);
    if (note) lines.push("【想怎麼改】" + note);
    eds.forEach(function(s){ lines.push("【改字】" + s.original + "  →  " + s.el.innerText.trim()); });
  });
  return lines.join("\n");
}

copyBtn.addEventListener("click", function(){
  var t = report();
  navigator.clipboard.writeText(t).then(function(){
    copyBtn.textContent = "已複製，直接貼給我";
    setTimeout(function(){ copyBtn.textContent = "複製全部修改"; }, 2200);
  }, function(){
    var w = window.open("", "_blank");
    w.document.write("<pre style='white-space:pre-wrap;font-size:15px;padding:20px'>" + esc(t) + "</pre>");
  });
});

document.getElementById("x-reset").addEventListener("click", function(){
  if (!confirm("清空這份 demo 的所有修改與註記？")) return;
  try { localStorage.removeItem(LSKEY); } catch (e) {}
  location.reload();
});
var tg = document.getElementById("x-toggle");
tg.addEventListener("click", function(){
  document.body.classList.toggle("x-marks");
  tg.textContent = document.body.classList.contains("x-marks") ? "隱藏虛線" : "顯示虛線";
});

document.addEventListener("input", refresh);

/* 目錄：一頁一頁跳 */
document.getElementById("x-toc").innerHTML =
  [].map.call(document.querySelectorAll(".x-row"), function(row, i){
    row.id = "b" + i;
    return '<a href="#b' + i + '">' + row.querySelector(".x-cap b").textContent.split("｜")[0] + "</a>";
  }).join("");

load();
refresh();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
