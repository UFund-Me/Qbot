#!/bin/bash

set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd -P)"
NEED_UPDATE="false"

function usage() {
  cat << EOF
Usage: $0 [options] ...
OPTIONS:
    -u, --update            Update the sysroot by manaul
    -h, --help              Show this message and exit
EOF
}

function parse_cmdline_args() {
  while [[ $# -gt 0 ]]; do
    local opt="$1"
    shift
    case "${opt}" in
      -u | --update)
        NEED_UPDATE="true"
        ;;
      -t | --test)
        python3 ${TOP_DIR}/core/bt_boll.py
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

}

main "$@"