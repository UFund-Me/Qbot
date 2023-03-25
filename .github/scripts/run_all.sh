#!/bin/bash

###
# @Author: Charmve yidazhang1@gmail.com
# @Date: 2023-01-20 23:48:48
# @LastEditors: Charmve yidazhang1@gmail.com
# @LastEditTime: 2023-03-26 01:06:11
# @FilePath: /Qbot/.github/scripts/run_all.sh
# @Version: 1.0.1
# @Blogs: charmve.blog.csdn.net
# @GitHub: https://github.com/Charmve
# @Description:
#
# Copyright (c) 2023 by Charmve, All Rights Reserved.
# Licensed under the MIT License.
###

set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd -P)"

function usage() {
  cat << EOF
Usage: $0 [options] ...
OPTIONS:
    -t, --test              Test strategies
    -u, --update            Update the sysroot by manaul
    -h, --help              Show this message and exit
EOF
}

function parse_cmdline_args() {
  while [[ $# -gt 0 ]]; do
    local opt="$1"
    shift
    case "${opt}" in
      -u | --update) ;;

      -t | --test)
        python "${TOP_DIR}"/qbot/strategies/bigger_than_ema_bt.py
        python "${TOP_DIR}"/qbot/strategies/boll_strategy_bt.py
        python "${TOP_DIR}"/qbot_main.py
        ;;
      -h | --help)
        usage
        exit 1
        ;;
    esac
  done
}

function main() {
  parse_cmdline_args "$@"

  echo "All done! ✨ 🍰 ✨"
}

main "$@"
