#! /usr/bin/env bash
set -eu

# Usage:
#       clang_format.sh <path/to/src/dir/or/files>

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# shellcheck disable=SC1090,SC1091
source "${TOP_DIR}/scripts/qbot_base.sh"

function check_clang_format() {
  if [[ -z "$(command -v clang-format)" ]]; then
    error "Command \"clang-format\" not found. Please make sure you are inside Dev Docker."
    exit 1
  fi
}

function clang_format_run() {
  # Rather than clang-format -i -style=Google "$@"
  # use settings specified in .clang-format
  clang-format -i -style=file "$@"
}

function find_c_cpp_srcs() {
  find "$@" -type f -name "*.h" \
    -o -name "*.c" \
    -o -name "*.hpp" \
    -o -name "*.cpp" \
    -o -name "*.hh" \
    -o -name "*.cc" \
    -o -name "*.hxx" \
    -o -name "*.cxx" \
    -o -name "*.cu"
}

function find_proto_srcs() {
  find "$@" -type f -name "*.proto" \
    -o -name "*.pb.txt"
}

function run_clang_format() {
  for target in "$@"; do
    if [[ -f "${target}" ]]; then
      if c_family_ext "${target}" || proto_ext "${target}"; then
        clang_format_run "${target}"
        info "Done formatting ${target}"
      else
        warning "Nothing to do. ${target} is not a c/c++/cuda/proto file"
      fi
    else
      find_proto_srcs "${target}" | xargs -r -n 100 -P 8 clang-format -i -style=file
      find_c_cpp_srcs "${target}" | xargs -r -n 100 -P 8 clang-format -i -style=file
      ok "Done formatting c/cpp/cuda/proto source files beneath directory '${target}'"
    fi
  done
}

function main() {
  check_clang_format

  if [ "$#" -eq 0 ]; then
    error "Usage: $0 <path/to/dirs/or/files>"
    exit 1
  fi

  run_clang_format "$@"
}

main "$@"
