#!/bin/bash
set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"

CI_MERGE_REQUEST_LABELS="${CI_MERGE_REQUEST_LABELS:-}"

function check_code_formatted() {
  readarray -t my_diffs < <(git diff \
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
  info "CI_MERGE_REQUEST_LABELS: ${CI_MERGE_REQUEST_LABELS}"
  check_merge_commit
  {
    IS_CI=true "${TOP_DIR}/scripts/format.sh" --git
  }
  check_code_formatted
}

main "$@"
