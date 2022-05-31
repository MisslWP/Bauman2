#!/bin/bash
f_in=$1
f_expect=$2
TEMP="out.temp"
APP="../../main.exe"

$APP < "$f_in" > "$TEMP"
res=$?

./comparator.sh "$TEMP" "$f_expect"
res=$?
rm "$TEMP"

if [ "$res" -eq 0 ]; then
    exit 0
fi
exit 1
