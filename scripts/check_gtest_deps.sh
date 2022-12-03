#!/bin/bash
set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# shellcheck disable=SC1091
source "${TOP_DIR}/scripts/qbot_base.sh"

function _is_target_testonly() {
  local target="$1"
  local testonly
  testonly="$(buildozer 'print testonly' "${target}")"
  [[ "${testonly}" == True || "${testonly}" == 1 ]]
}

function _is_gtest_dependent_target() {
  local deps
  deps="$(buildozer 'print deps' "$1" 2> /dev/null)"
  # NOTE:
  # Here we can check ONLY direct dependency on googletest.
  # Since if target_b depends on target_a which in turn depends on gtest
  # Bazel will emit the following error:
  # >> non-test target 'target_b' depends on testonly target 'target_a'
  # >> and doesn't have testonly attribute set
  [[ "${deps}" == *"@com_google_googletest//:"* ]]
}

function _testonly_check_for_gtest_dependent_target() {
  local target="$1"
  if ! _is_gtest_dependent_target "${target}"; then
    return
  fi

  if ! _is_target_testonly "${target}"; then
    error "testonly=True unspecified for gtest-dependent target ${target}"
    return 1
  fi
}

function gtest_dependency_check_for_dir() {
  local dir="$1"
  local recursive="${2:-false}"

  local readonly NON_TEST_CC_PATTERNS=(
    "%cc_library"
    "%cc_binary"
    "%cuda_library"
    "%cuda_binary"
    "%qt_cc_library"
  )

  local prefix
  if [[ "${recursive}" == true ]]; then
    prefix="//${dir}/..."
  else
    prefix="//${dir}"
  fi

  # Since bazel query is relative slow (esp. on CI), instead of querying all
  # targets that deps on gtest with something like:
  # bazel query "rdeps(//onboard/...:all, @com_google_googletest//:gtest)" 2> /dev/null
  # bazel query "rdeps(//onboard/...:all, @com_google_googletest//:gtest_prod)" 2> /dev/null
  # we can query deps of all {cc,cuda}_{library,binary} and qt_cc_library targets to see if
  # one of them starts with @com_google_googletest
  for rule_patt in "${NON_TEST_CC_PATTERNS[@]}"; do
    while read -r target; do
      _testonly_check_for_gtest_dependent_target "${target}"
    done < <(buildozer 'print label' "${prefix}:${rule_patt}")
  done

  ok "Done checking gtest dependency for ${prefix}"
}

function main() {
  sub_dirs=(onboard offboard third_party experimental) # cyber cyber_modules
  for dir in "${sub_dirs[@]}"; do
    gtest_dependency_check_for_dir "${dir}" true
  done
}

# Used both as Bash library and binary
if [[ "$0" == "${BASH_SOURCE[0]}" ]]; then
  main "$@"
fi
