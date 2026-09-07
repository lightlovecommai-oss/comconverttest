#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# 共用件同步器（atpi-core.js／track.js）
#
# 為什麼要有這支：這兩個檔的程式真相只有一份，都在
#   4-溝通健身房/consult-workshop/
# 但 comconverttest 是**獨立 repo、獨立 GitHub Pages 站台**，
# 沒辦法直接 <script src> 到另一個 repo 的檔案（相對路徑在本機與線上不一致），
# 所以這裡放**同步副本**，靠這支腳本複製、不靠手改。
#
#   ./sync-atpi-core.sh          # 檢查有沒有跟真相檔漂掉（不改檔）
#   ./sync-atpi-core.sh --write  # 從真相檔複製過來
#
# ⚠️ 規矩：要改 ATPI 定義或追蹤邏輯**永遠改 consult-workshop 那份**，再跑這支拉過來。
#    絕對不要直接編輯本 repo 的副本——下次同步會被蓋掉。
# ─────────────────────────────────────────────────────────────
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRCDIR="$HERE/../../4-溝通健身房/consult-workshop"
FILES=(atpi-core.js track.js)

drift=0
for f in "${FILES[@]}"; do
  SRC="$SRCDIR/$f"
  DST="$HERE/$f"
  if [ ! -f "$SRC" ]; then
    echo "❌ 找不到真相檔：$SRC"
    echo "   （consult-workshop 沒 clone 在隔壁的話，請自己指定路徑再複製）"
    exit 1
  fi
  if diff -q "$SRC" "$DST" >/dev/null 2>&1; then
    echo "✅ $f 與真相檔一致"
    continue
  fi
  if [ "${1:-}" = "--write" ]; then
    cp "$SRC" "$DST"
    echo "✅ 已同步 $f —— 記得 git add && commit"
  else
    echo "⚠️  $f 已與真相檔漂掉，差異如下："
    diff "$DST" "$SRC" || true
    echo ""
    drift=1
  fi
done

if [ "$drift" = 1 ]; then
  echo "→ 要拉過來就跑：./sync-atpi-core.sh --write"
  exit 1
fi
