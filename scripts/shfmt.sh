#! /usr/bin/env bash
# Usage:
#   shfmt.sh <path/to/src/dir/or/files>
set -eu

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# shellcheck disable=SC1090,SC1091
source ${TOP_DIR}/scripts/qbot_base.sh

SHELL_FORMAT_CMD="shfmt"

function _find_shell_srcs() {
  find "$@" -type f -name "*.sh" \
    -o -name "*.bash"
}

function check_shfmt() {
  if [ -z "$(command -v shfmt)" ]; then
    error "Oops, shfmt missing..."
    error "Please make sure shfmt is installed and check your PATH settings."
    exit 1
  fi
}

function shell_format_run() {
  # Use settings in .editorconfig
  ${SHELL_FORMAT_CMD} -w "$@"
  for path in "$@"; do
    local bang
    bang="$(head -c 2 "${path}")"
    if [[ "${bang}" != "#!" ]]; then
      warning "No shebang for ${path}. Fix automatically." >&2
      sed -i '1s;^;#! /bin/bash\n;' "${path}"
      ok "Done fix shebang on ${path}"
    fi
  done
}

function run_shfmt() {
  for target in "$@"; do
    if [ -f "${target}" ]; then
      if bash_ext "${target}"; then
        shell_format_run "${target}"
        ok "Done formatting ${target}"
      else
        warning "Do nothing. ${target} is not a Bash script."
      fi
    else
      local srcs
      srcs="$(_find_shell_srcs ${target})"
      if [ -z "${srcs}" ]; then
        ok "No need to format Bash scripts beneath ${target} as none found"
        continue
      fi
      shell_format_run ${srcs}
      ok "Done formatting Bash scripts beneath ${target}"
    fi
  done
}

function main() {
  check_shfmt

  if [ "$#" -eq 0 ]; then
    error "Usage: $0 <path/to/dirs/or/files>"
    exit 1
  fi

  run_shfmt "$@"
}

main "$@"
