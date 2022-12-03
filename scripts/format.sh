#! /usr/bin/env bash
# Usage:
#   scripts/format.sh [options] <path/to/src/dirs/or/files>
# OR:
#   scripts/format.sh --git
#
# The git mode was inspired by the original clang-fix.sh.
# Here we choose `git diff HEAD` and submodules ignored.
# Reference: `git help diff`:
#EXAMPLES
#  Various ways to check your working tree
#
#  $ git diff            (1)
#  $ git diff --cached   (2)
#  $ git diff HEAD       (3)
#
#  1. Changes in the working tree not yet staged for the next commit.
#  2. Changes between the index and your last commit; what you would be
#     committing if you run "git commit" without "-a" option.
#  3. Changes in the working tree since your last commit; what you would
#     be committing if you run "git commit -a"
#
set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# shellcheck disable=SC1091
source "${TOP_DIR}/scripts/qbot_base.sh"

GIT_MODE=0
IS_CI="${IS_CI:-false}"

FORMAT_BAZEL=0
FORMAT_CPP=0
FORMAT_PYTHON=0
FORMAT_BASH=0
FORMAT_GO=0
FORMAT_ALL=0
SKIP_STR_NORM_PY=0
HAS_OPTION=0

function print_usage() {
  echo -e "${RED}Usage${NO_COLOR}:
    ${BOLD}$0${NO_COLOR} --git ${BLUE}# Format changed files${NO_COLOR}
  OR:
    ${BOLD}$0${NO_COLOR} [OPTION] <path/to/src/dir/or/files>"
  echo -e "\n${RED}Options${NO_COLOR}:
  ${BLUE}-p|--python          ${NO_COLOR}Format Python sources.
  ${BLUE}-B|--bazel           ${NO_COLOR}Format Bazel files.
  ${BLUE}-c|--cpp             ${NO_COLOR}Format C/C++/Proto sources.
  ${BLUE}-b|--bash            ${NO_COLOR}Format Bash scripts.
  ${BLUE}-g|--go              ${NO_COLOR}Format Go sources.
  ${BLUE}-S|skip-str-norm-py  ${NO_COLOR}Don't normalize string quotes or prefixes for Python
  ${BLUE}-a|--all             ${NO_COLOR}Format all.
  ${BLUE}-h|--help            ${NO_COLOR}Show this message and exit."
}

function run_clang_format() {
  bash "${TOP_DIR}/scripts/clang_format.sh" "$@"
}

function run_pyfmt() {
  bash "${TOP_DIR}/scripts/pyfmt.sh" "$@"
}

function run_shfmt() {
  bash "${TOP_DIR}/scripts/shfmt.sh" "$@"
}

function run_gofmt() {
  bash "${TOP_DIR}/scripts/gofmt.sh" "$@"
}

function run_format() {
  for arg in "$@"; do
    if [[ -f "${arg}" ]]; then
      # if c_family_ext "${arg}" || proto_ext "${arg}"; then
      #   run_clang_format "${arg}"
      if plain_py_ext "${arg}"; then
        if [[ "${IS_CI}" == true || "${SKIP_STR_NORM_PY}" -eq 1 ]]; then
          run_pyfmt -S "${arg}"
        else
          run_pyfmt "${arg}"
        fi
      elif bash_ext "${arg}"; then
        run_shfmt "${arg}"
      elif go_ext "${arg}"; then
        run_gofmt "${arg}"
      fi
    elif [[ -d "${arg}" ]]; then
      if [[ "${FORMAT_CPP}" -eq 1 ]]; then
        run_clang_format "${arg}"
      fi
      if [[ "${FORMAT_PYTHON}" -eq 1 ]]; then
        if [[ "${IS_CI}" == true || "${SKIP_STR_NORM_PY}" -eq 1 ]]; then
          run_pyfmt -S "${arg}"
        else
          run_pyfmt "${arg}"
        fi
      fi
      if [[ "${FORMAT_BASH}" -eq 1 ]]; then
        run_shfmt "${arg}"
      fi
      if [[ "${FORMAT_GO}" -eq 1 ]]; then
        run_gofmt "${arg}"
      fi
    else
      warning "Ignored ${arg} as not a regular file/directory"
    fi
  done
}

function main() {
  if [ "$#" -eq 0 ]; then
    print_usage
    exit 1
  fi

  while [[ $# -gt 0 ]]; do
    local opt="$1"
    case "${opt}" in
      -p | --python)
        FORMAT_PYTHON=1
        HAS_OPTION=1
        shift
        ;;
      -c | --cpp)
        FORMAT_CPP=1
        HAS_OPTION=1
        shift
        ;;
      -B | --bazel)
        FORMAT_BAZEL=1
        HAS_OPTION=1
        shift
        ;;
      -b | --bash)
        FORMAT_BASH=1
        HAS_OPTION=1
        shift
        ;;
      -g | --go)
        FORMAT_GO=1
        HAS_OPTION=1
        shift
        ;;
      -S | --skip-str-norm-py)
        SKIP_STR_NORM_PY=1
        shift
        ;;
      -a | --all)
        FORMAT_ALL=1
        shift
        ;;
      --git)
        GIT_MODE=1
        FORMAT_ALL=1
        shift
        ;;
      -h | --help)
        print_usage
        exit 1
        ;;
      *)
        if [[ "${opt}" == -* ]]; then
          print_usage
          exit 1
        else
          if [[ "$HAS_OPTION" -eq 0 ]]; then
            FORMAT_ALL=1
          fi
          break
        fi
        ;;
    esac
  done

  if [ "${FORMAT_ALL}" -eq 1 ]; then
    # shellcheck disable=SC2034
    FORMAT_BAZEL=1
    FORMAT_CPP=1
    FORMAT_BASH=1
    FORMAT_GO=1
    FORMAT_PYTHON=1
  fi

  if [[ "${GIT_MODE}" -eq 1 ]]; then

    # Note:
    # 1) Exclude deleted files, Ref:
    #    https://stackoverflow.com/questions/6894322/how-to-make-git-diff-and-git-log-ignore-new-and-deleted-files
    # 2) git-clang-format Ref:
    #    https://github.com/llvm/llvm-project/blob/release/12.x/clang/tools/clang-format/git-clang-format
    local what_to_diff
    what_to_diff="${CI_MERGE_REQUEST_DIFF_BASE_SHA:-HEAD~1}"

    # readarray -t diff_files < <(git diff --ignore-submodules --diff-filter=d --name-only "${what_to_diff}")
    ## instead of readarray
    # shellcheck disable=SC1001,SC2162
    while IFS=\= read diff_file; do
      diff_files+=("$diff_file")
    done < <(git diff --ignore-submodules --diff-filter=d --name-only "${what_to_diff}")

    for one_change in "${diff_files[@]}"; do
      run_format "${TOP_DIR}/${one_change}"
    done

    bash "${TOP_DIR}/scripts/format_extra_check.sh"
  else
    run_format "$@"
  fi
}

main "$@"
