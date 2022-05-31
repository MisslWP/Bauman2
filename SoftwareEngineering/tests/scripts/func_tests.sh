#!/bin/bash

data_path="../data"
app="../../main.exe"
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

ERR=255

in_raw=$(find $data_path -name "in_[0-9][0-9].txt" | sort | tr '\n' ' ')
out_raw=$(find $data_path -name "out_[0-9][0-9].txt" | sort | tr '\n' ' ')

IFS=' ' read -r -a in <<< "$in_raw"
IFS=' ' read -r -a out <<< "$out_raw"

in_c=${#in[@]}
out_c=${#out[@]}
failed=0

if [ "$in_c" -ne "$out_c" ]; then
    echo "in and out files count is not equal! Aborting tests..."
    exit $ERR
fi

if [ ! -f "$app" ]; then
    echo "Cannot find $app, please compile the program!"
    exit $ERR
fi

echo "Starting tests:"

for i in "${!in[@]}"; do
    echo $"Test ${in[$i]}"
    ./test.sh "${in[$i]}" "${out[$i]}"
    res=$?
    if [ $res -eq 0 ]; then
        echo -e "TEST: ${GREEN}PASSED${NC}"
    else
        echo -e "TEST: ${RED}FAILED${NC}"
        failed=$((failed+1))
    fi
done

echo "Tests passed: $((in_c - failed))/$in_c"

exit $failed
