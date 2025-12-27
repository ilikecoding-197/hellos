#!/bin/bash

OUT=out
ALL_LANGS=0
VALID_LANGS=0

check() {
	local LANG="$1"
	((ALL_LANGS++))

	VAILD=0
	diff "out/$LANG.txt" good.txt -q > /dev/null && VAILD=1 || echo "$LANG invalid"

	if (( VAILD == 1)); then
		echo "$LANG valid"
		((VALID_LANGS++))
	fi
}

while IFS= read -r line; do
    check "$line"
done < <(find out -maxdepth 1 -type f -exec basename {} .txt \;)

echo
echo "$VALID_LANGS/$ALL_LANGS languages are vaild"
