#!/bin/bash
set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
# shellcheck disable=SC1090,SC1091
source "${TOP_DIR}/scripts/check_gtest_deps.sh"

function check_code_formatted() {
  local my_diffs=()
  # shellcheck disable=SC1001,SC2162
  while IFS=\= read my_diff; do
    my_diffs+=("$my_diff")
  done < <(git diff \
    --ignore-submodules --diff-filter=d --name-only -- \
    "*.h" "*.cc" "*.cpp" "*.cu" \
    "*.proto" \
    "*.py" \
    "*[./]BUILD" "*.bzl" "BUILD" "WORKSPACE" \
    "*.sh")

  if (("${#my_diffs[@]}" > 0)); then
    error "Format issue found:"
    # Show complete diff for end users
    for myf in "${my_diffs[@]}"; do
      git diff "${myf}"
    done
    error "Please run either of the following commands to fix them before commit."
    info "  1) scripts/format.sh --git"
    info "OR"
    info "  2) scripts/format.sh ${my_diffs[*]}"
    exit 1
  else
    ok "Congrats! Format check passed."
    exit 0
  fi
}

function check_merge_commit() {
  local from_to
  if [[ -n "${CI_MERGE_REQUEST_DIFF_BASE_SHA:-}" ]]; then
    from_to="${CI_MERGE_REQUEST_DIFF_BASE_SHA}..HEAD"
  else
    from_to="HEAD~1..HEAD"
  fi
  local msg=
  msg="$(git log "${from_to}" --merges 2> /dev/null)"
  if [[ -n "${msg}" ]]; then
    error "Merge commit should not exist in dev branch, please squash it first."
    info "${msg}"
    exit 1
  fi
  ok "This MR is not a merge commit."
}

function main() {
  check_merge_commit
  {
    IS_CI=true "${TOP_DIR}/scripts/format.sh" --git
  }
  check_code_formatted
}

main "$@"
