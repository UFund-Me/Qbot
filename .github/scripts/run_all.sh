#!/bin/bash

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
        python "${TOP_DIR}"/core/bt_boll.py
        python "${TOP_DIR}"/core/bt_bigger_than_EMA.py
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
