#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# atpi-core.js 同步器
#
# 為什麼要有這支：ATPI 的程式真相只有一份，在
#   4-溝通健身房/consult-workshop/atpi-core.js
# 但 comconverttest 是**獨立 repo、獨立 GitHub Pages 站台**，
# 沒辦法直接 <script src> 到另一個 repo 的檔案（相對路徑在本機與線上不一致），
# 所以這裡放一份**同步副本**，靠這支腳本複製、不靠手改。
#
#   ./sync-atpi-core.sh          # 檢查有沒有跟真相檔漂掉（不改檔）
#   ./sync-atpi-core.sh --write  # 從真相檔複製過來
#
# ⚠️ 規矩：要改 ATPI 定義**永遠改 consult-workshop 那份**，再跑這支拉過來。
#    絕對不要直接編輯本 repo 的 atpi-core.js——下次同步會被蓋掉。
# ─────────────────────────────────────────────────────────────
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/../../4-溝通健身房/consult-workshop/atpi-core.js"
DST="$HERE/atpi-core.js"

if [ ! -f "$SRC" ]; then
  echo "❌ 找不到真相檔：$SRC"
  echo "   （consult-workshop 沒 clone 在隔壁的話，請自己指定路徑再複製）"
  exit 1
fi

if diff -q "$SRC" "$DST" >/dev/null 2>&1; then
  echo "✅ atpi-core.js 與真相檔一致"
  exit 0
fi

if [ "${1:-}" = "--write" ]; then
  cp "$SRC" "$DST"
  echo "✅ 已從 consult-workshop 同步 atpi-core.js —— 記得 git add && commit"
else
  echo "⚠️  atpi-core.js 已與真相檔漂掉，差異如下："
  diff "$DST" "$SRC" || true
  echo ""
  echo "→ 要拉過來就跑：./sync-atpi-core.sh --write"
  exit 1
fi
