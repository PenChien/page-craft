#!/usr/bin/env bash
# 發布 HTML 到 static.example.com portal。
#   publish.sh <site> <本機檔> <線上名> [--index]
# token 讀 ~/.config/space-portal.env 的 SPACE_TOKEN=<token>；不印出、不進對話。
set -euo pipefail
SITE=${1:?usage: publish.sh <site> <src-file> <served-name> [--index]}
SRC=${2:?src file}; NAME=${3:?served filename}
ENVF=$HOME/.config/space-portal.env
[ -f "$ENVF" ] || { echo "missing $ENVF (put SPACE_TOKEN=<token> in it, chmod 600)"; exit 1; }
TOK=$(grep -m1 -E '^SPACE_TOKEN=' "$ENVF" | cut -d= -f2- | tr -d '"'"'"' ')
[ -n "$TOK" ] || { echo "SPACE_TOKEN not found in $ENVF"; exit 1; }
[ -f "$SRC" ] || { echo "src not found: $SRC"; exit 1; }
API=https://portal.static.example.com/api/v1
curl -sS --fail-with-body -o /dev/null -w "upload $NAME HTTP %{http_code}\n" \
  -H "Authorization: Bearer $TOK" -F "files=@$SRC;filename=$NAME" "$API/sites/$SITE/files"
# cmp verify (portal 大檔有延遲，重試)
URL="https://$SITE.static.example.com/$NAME"; T=$(mktemp)
for i in 1 2 3 4 5; do sleep 3; curl -sS "$URL" -o "$T"; cmp -s "$T" "$SRC" && break; done
if cmp -s "$T" "$SRC"; then echo "served == local ($(stat -c %s "$SRC") bytes)"; else echo "MISMATCH served vs local"; fi
rm -f "$T"
if [ "${4:-}" = "--index" ]; then
  curl -sS -o /dev/null -w "set index HTTP %{http_code}\n" -H "Authorization: Bearer $TOK" \
    -X PUT -H 'Content-Type: application/json' -d "{\"file\":\"$NAME\"}" "$API/sites/$SITE/index"
fi
echo "$URL"
