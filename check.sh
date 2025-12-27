#!/usr/bin/env bash

OUT=out
ALL_LANGS=0
VALID_LANGS=0

check() {
    local LANG="$1"
    ((ALL_LANGS++))

    if diff "$OUT/$LANG.txt" good.txt -q > /dev/null; then
        echo "$LANG valid"
        ((VALID_LANGS++))
    else
        echo "$LANG invalid"
    fi
}

for file in "$OUT"/*.txt; do
    [[ -e "$file" ]] || continue
    check "$(basename "$file" .txt)"
done

echo
echo "$VALID_LANGS/$ALL_LANGS languages are valid"
