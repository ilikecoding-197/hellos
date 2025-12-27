#!/usr/bin/env bash

SRC=src
BUILD=build
OUT=out

rm -rf "$BUILD" && mkdir "$BUILD"
rm -rf "$OUT" && mkdir "$OUT"

gcc -o "$BUILD/c" "$SRC/hello.c" && echo "hello.c built"
g++ -o "$BUILD/cpp" "$SRC/hello.cpp" && echo "hello.cpp built"

echo

run() {
	local CMD="$1"
	local LANG="$2"

	$CMD > "$OUT/$LANG.txt" && echo "$LANG succeeded" || echo "$LANG failed"
}

run "$BUILD/c" c
run "$BUILD/cpp" cpp
run "$SRC/hello.sh" sh
run "python3 $SRC/hello.py" py
run "node $SRC/hello.js" js
