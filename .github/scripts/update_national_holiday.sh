#!/bin/bash

set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd -P)"
_file="${TOP_DIR}/config/national_holidays.csv"

function parse_holiday() {
    cron_items={}
    cron_items+="$(grep '2022' national_holidays.csv | awk -F ',' '{print $3, $4}' | awk -F '-' '{print $3, $2, $1, $4}' | awk  -F ' ' '{print 00, 9, $4, $2}')" + " *"
    cron_items+="$(grep '2022' national_holidays.csv | awk -F ',' '{print $3, $4}' | awk -F '-' '{print $3, $2, $1, $4}' | awk  -F ' ' '{print 00, 9, $3, $1}')" + " *"
    
    line=$(grep -n "cron" ../workflows/auto_trade.yml | cut -d ":" -f 1)
    echo ${line}

    for cron_items in  ${cron_items[@]}
    do
        sed -i "${line}c     - cron: '${cron_item}' " auto_trade.yml
    done
}

function main() {
    ## get holidays
    python ../../scripts/statutory_holiday_process.py

    ## parse_holiday
    parse_holiday
}

main "$@"