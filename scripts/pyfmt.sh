#!/usr/bin/env bash

# Usage:
#   pyfmt.sh <path/to/python/dir/or/files>
set -eu

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# shellcheck disable=SC1090,SC1091
source "${TOP_DIR}/scripts/qbot_base.sh"

SKIP_STRING_NORMALIZATION=false

function check_cmd_existence() {
  for cmd in "$@"; do
    if [[ -z "$(command -v "${cmd}")" ]]; then
      error "Command '${cmd}' not found. Install it manually by running: "
      error "  sudo -H pip3 install --upgrade --no-cache-dir ${cmd}"
      exit 1
    fi
  done
}

function find_plain_py_srcs() {
  find "$@" -type f -name "*.py" -and ! -name "*_pb2.py" -and ! -name "*_pb2_grpc.py"
}

function black_run() {
  if [[ "${SKIP_STRING_NORMALIZATION}" == true ]]; then
    black --skip-string-normalization "$@"
  else
    black "$@"
  fi
}

function pyfmt_run() {
  isort "$@"
  black_run "$@"
  flake8 "$@" # --exit-zero removed to enforce
}

function run_pyfmt() {
  for target in "$@"; do
    if [ -f "${target}" ]; then
      if plain_py_ext "${target}"; then
        pyfmt_run "${target}"
        ok "Done formatting ${target}"
      else
        warning "Nothing to do. ${target} is not a (regular) Python file."
      fi
    else
      while read -r file_ent; do
        pyfmt_run "${file_ent}"
      done < <(find_plain_py_srcs "${target}")
      ok "Done formatting Python files under ${target}"
    fi
  done
}

function usage() {
  info "Usage: $0 [-S] <path/to/python/dirs/or/files>"
}

function main() {
  check_cmd_existence "isort" "black" "flake8"

  local dirs_or_files=()

  while [[ $# -gt 0 ]]; do
    local arg
    arg="$1"
    shift
    case "${arg}" in
      -S)
        SKIP_STRING_NORMALIZATION=true
        ;;
      -h | --help)
        usage
        exit 0
        ;;
      -*)
        error "Unknown option: ${arg}"
        usage
        exit 1
        ;;
      *)
        dirs_or_files+=("${arg}")
        ;;
    esac
  done

  run_pyfmt "${dirs_or_files[@]}"
}

main "$@"
