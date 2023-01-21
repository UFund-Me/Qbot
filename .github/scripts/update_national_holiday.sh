#!/bin/bash

# ****************************************************************************
#  Update China national holidays every year
#  Author: Charmve
#
#  Copyright 2022 Charmve. All Rights Reserved.
#  Licensed under the MIT License.
# ****************************************************************************

set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd -P)"
_file="${TOP_DIR}/qbot/config/national_holidays.csv"

function parse_holiday() {
  local cron_items=()
  cron_items+=("$(grep '2022' "${_file}" | awk -F ',' '{print $3, $4}' | awk -F '-' '{print $3, $2, $1, $4}' | awk -F ' ' '{print 00, 9, $4, $2}')" + " *")
  cron_items+=("$(grep '2022' "${_file}" | awk -F ',' '{print $3, $4}' | awk -F '-' '{print $3, $2, $1, $4}' | awk -F ' ' '{print 00, 9, $3, $1}')" + " *")

  line=$(grep -n "cron" "${TOP_DIR}/.github/workflows/auto_trade.yml" | cut -d ":" -f 1)
  echo "${line}"

  for cron_item in "${cron_items[@]}"; do
    sed -i "${line}c     - cron: '${cron_item}' " "${TOP_DIR}/.github/workflows/auto_trade.yml"
  done
}

function main() {
  ## get holidays
  python ../../scripts/statutory_holiday_process.py

  ## parse_holiday
  parse_holiday
}

main "$@"
