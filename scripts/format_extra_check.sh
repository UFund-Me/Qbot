#! /bin/bash
set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# shellcheck disable=SC1090,SC1091
source "${TOP_DIR}/scripts/qbot_base.sh"
# shellcheck disable=SC1090,SC1091
source "${TOP_DIR}/scripts/check_gtest_deps.sh"

SHELL_CHECK_GIST="https://gist.github.com/nicerobot/53cee11ee0abbdc997661e65b348f375#file-_shellcheck-md"

############################ Internal Functions ##############################
function _check_if_dir_is_proto_specific() {
  local dir="$1"
  readarray -t files < <(ls "${dir}")
  for myf in "${files[@]}"; do
    if [[ "${myf}" == *".proto" || "${myf}" == "BUILD" ]] || [[ "${myf}" == *".md" ]] || [[ -d "${dir}/${myf}" ]]; then
      : # It's OK
    else
      error "Non-proto file found in (supposed) proto-specific dir ${dir}: ${myf}"
      return 1
    fi
  done
}

function run_gtest_dependency_check() {
  local fn="$1"
  if [[ "${fn}" == BUILD || "${fn}" == */BUILD ]]; then
    local dir=
    if [[ "${fn}" == */BUILD ]]; then
      dir="$(dirname "${fn}")"
    fi
    gtest_dependency_check_for_dir "${dir}"
  fi
}

function proto_specific_dirs_check() {
  declare -a proto_dirs=()
  for fn in "$@"; do
    if [[ "${fn}" == *".proto" ]]; then
      local dir
      dir="$(dirname "${TOP_DIR}/${fn}")"
      proto_dirs["$dir"]=1
    fi
  done
  for dir in "${!proto_dirs[@]}"; do
    _check_if_dir_is_proto_specific "${dir}"
    ok "Done proto-specific dir check on ${dir}"
  done
}

function run_proto_lint() {
  local msg
  # NOTE:
  # 1. run "buf lint" from top_dir
  # 2. buf lint would probably fail, here we check unused imports only
  pushd "${TOP_DIR}" > /dev/null
  msg="$(buf lint --path "$1" | grep -E "Import .* is unused")" || true
  popd > /dev/null
  if [[ -n "${msg}" ]]; then
    error "${msg}"
    return 1
  fi
}

function run_shellcheck() {
  local fn="$1"
  if ! shellcheck -x "${fn}"; then
    error "Running 'shellcheck -x ${fn}' returned non-zero exit status."
    error "Please fix it first."
    info "For all shellcheck codes, please visit: ${SHELL_CHECK_GIST}"
    return 1
  fi
}

function main() {
  local what_to_diff
  what_to_diff="${CI_MERGE_REQUEST_DIFF_BASE_SHA:-HEAD~1}"

  # readarray -t changes < <(git diff --ignore-submodules --diff-filter=d --name-only "${what_to_diff}")
  # shellcheck disable=SC1001,SC2162
  while IFS=\= read change; do
    changes+=("$change")
  done < <(git diff --ignore-submodules --diff-filter=d --name-only "${what_to_diff}")

  for one_change in "${changes[@]}"; do
    if [[ "${one_change}" == *".proto" ]]; then
      run_proto_lint "${one_change}"
    elif bash_ext "${one_change}"; then
      run_shellcheck "${TOP_DIR}/${one_change}"
    fi
    run_gtest_dependency_check "${one_change}"
  done
  proto_specific_dirs_check "${changes[@]}"
}

main "$@"
