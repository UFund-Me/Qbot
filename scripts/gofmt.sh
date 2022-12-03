#! /bin/bash
# Usage:
#  scripts/gofmt.sh <path/to/dir/files>
set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# shellcheck disable=SC1090,SC1091
source "${TOP_DIR}/scripts/qbot_base.sh"

GOFMT_PATH=
function check_gofmt_cmd() {
  if ! inside_docker; then
    if [[ -z "$(command -v gofmt)" ]]; then
      error "Command \"gofmt\" not found."
      error "Please either make sure gofmt is installed, or run inside Docker."
      exit 1
    fi
    GOFMT_PATH="$(command -v gofmt)"
  else # Inside Docker
    if [[ -z "$(command -v bazel)" ]] || ! bazel info workspace &> /dev/null; then
      warning "Command \"bazel\" not found or not run from within Bazel workspace"
      warning "Looking for gofmt binary from PATH settings..."
      if [[ -z "$(command -v gofmt)" ]]; then
        error "Command \"gofmt\" not found inside Docker"
        exit 1
      else
        GOFMT_PATH="$(command -v gofmt)"
      fi
    else
      # NOTE: This depends on two facts:
      # 1) Our workspace is named com_Qbot and its workspace dir /Qbot is writable
      # 2) The symlink created (pointing to the execution_root dir) is Qbot
      #    bazel info execution_root
      # Ref to https://docs.bazel.build/versions/main/user-manual.html on execution_root
      GOFMT_PATH="${TOP_DIR}/Qbot/external/go_sdk/bin/gofmt"
      [[ -f "${GOFMT_PATH}" ]] || bazel build -c opt @go_sdk//:bin/gofmt
    fi
  fi # Done Inside Docker
  info "Using gofmt: ${GOFMT_PATH}"
}

function run_gofmt {
  for target in "$@"; do
    if [[ -f "${target}" ]]; then
      if go_ext "${target}"; then
        "${GOFMT_PATH}" -w "${target}"
        ok "Done formatting ${target}"
      else
        warning "Nothing to do. ${target} is not Go file."
      fi
    elif [[ -d "${target}" ]]; then
      find "${target}" -name "*.go" -exec "${GOFMT_PATH}" -w {} \;
      ok "Done formatting Go source files beneath \"${target}\""
    fi
  done
}

function main() {
  check_gofmt_cmd
  if [[ $# -eq 0 ]]; then
    error "Usage: $0 <path/to/dirs/or/files>"
    exit 1
  fi

  run_gofmt "$@"
}

main "$@"
