#!/usr/bin/env bash
# 刪 static.example.com portal 上的檔。
#   delete.sh <site> <path>
# token 讀 ~/.config/space-portal.env；不印出。
set -euo pipefail
SITE=${1:?usage: delete.sh <site> <path>}; P=${2:?path}
TOK=$(grep -m1 -E '^SPACE_TOKEN=' "$HOME/.config/space-portal.env" | cut -d= -f2- | tr -d '"'"'"' ')
[ -n "$TOK" ] || { echo "SPACE_TOKEN not found"; exit 1; }
code=$(curl -sS -o /dev/null -w '%{http_code}' -X DELETE -H "Authorization: Bearer $TOK" \
  "https://portal.static.example.com/api/v1/sites/$SITE/files/$P")
echo "delete $P HTTP $code"
sleep 2
curl -sS -o /dev/null -w "verify (expect 404) HTTP %{http_code}\n" "https://$SITE.static.example.com/$P"
