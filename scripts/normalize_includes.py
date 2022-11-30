#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import re
import sys
from pathlib import Path

C_OR_CPP_EXTENSIONS = [".h", ".hpp", ".cc", ".cpp", ".c", ".cu", ".cuh"]
INCLUDE_LINE_PATT = re.compile(r'#include (["<][\w+/]+.\w+[">])(.*)')
NOLINT_TEXT = " // NOLINT"


QUOTATION_CORPUS = None
BRACKET_CORPUS = None
QT_MODULES = None
QT_HEADER_MAPPINGS = None


def _no_lint_comment(comment):
    return comment if NOLINT_TEXT in comment else NOLINT_TEXT


def _load_corpus_impl(data_relative_path):
    pathent = Path(__file__).parent.joinpath(data_relative_path)
    if not pathent.exists() or not pathent.is_file():
        logging.error(f"Non-existent-or-not-a-file: {pathent}")
        return None
    with open(pathent, encoding="utf-8") as fin:
        return set(line.strip() for line in fin if not line.startswith("#"))


def load_quotation_corpus():
    global QUOTATION_CORPUS
    QUOTATION_CORPUS = _load_corpus_impl("data/quotes.txt")
    return QUOTATION_CORPUS


def load_qt_header_mappings():
    global QT_HEADER_MAPPINGS

    pathent = Path(__file__).parent.joinpath("data/qt_headers.json")
    if not pathent.exists() or not pathent.is_file():
        logging.error(f"Non-existent-or-not-a-file: {pathent}")
        QT_HEADER_MAPPINGS = None

    with open(pathent, encoding="utf-8") as fin:
        QT_HEADER_MAPPINGS = json.load(fin)

    return QT_HEADER_MAPPINGS


def load_bracket_corpus():
    global BRACKET_CORPUS
    BRACKET_CORPUS = _load_corpus_impl("data/standard_headers.txt")
    return BRACKET_CORPUS


def load_qt_modules():
    global QT_MODULES
    QT_MODULES = _load_corpus_impl("data/qt_modules.txt")
    return QT_MODULES


def normalize_include_line(include, comment):
    # quote = include[0] == '"'
    header = include[1:-1]
    if header in BRACKET_CORPUS:
        return f"#include <{header}>{comment}"
    elif header in QT_HEADER_MAPPINGS:
        normalized = QT_HEADER_MAPPINGS[header]
        comment = _no_lint_comment(comment)
        return f"#include <{normalized}>{comment}"
    elif "/" in header:
        package = header.split("/")[0]
        if package in QT_MODULES:
            comment = _no_lint_comment(comment)
            return f"#include <{header}>{comment}"
        if package in QUOTATION_CORPUS:
            return f'#include "{header}"{comment}'
    return f"#include {include}{comment}"


def normalize_header_includes(fentry, dry=False, strip=False):
    lines = []
    logging.info(f"Processing {fentry} ...")

    with open(fentry, encoding="utf-8") as fin:
        if strip:
            already_included = set()

        for line in fin:
            match = INCLUDE_LINE_PATT.match(line)
            if not match:
                lines.append(line)
                continue
            quoted_inc = match.group(1)
            line = normalize_include_line(quoted_inc, match.group(2))

            if strip:
                unquoted_inc = quoted_inc[1:-1]
                if unquoted_inc in already_included:
                    logging.info(f"{fentry}: {quoted_inc} already included previously.")
                    logging.info("  Please keep the include-one-header-only-once rule.")
                    continue

                already_included.add(unquoted_inc)
            if dry:
                print(line, file=sys.stderr)

            lines.append(line + "\n")
    if not dry and lines:
        with open(fentry, "w", encoding="utf-8") as fout:
            fout.writelines(lines)


# TODO: maybe a multi-threaded version
def main(files=None, dirs=None, dry=False, strip=False):
    if files:
        for ent in files:
            normalize_header_includes(ent, dry=dry, strip=strip)
    if dirs:
        for dirent in dirs:
            matches = [
                p.resolve()
                for p in dirent.glob("**/*")
                if p.suffix in C_OR_CPP_EXTENSIONS
            ]
            for ent in matches:
                normalize_header_includes(ent, dry=dry, strip=strip)


if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dry",
        action="store_true",
        help="Run this script in dry-run mode.",
    )
    parser.add_argument(
        "-s",
        "--strip",
        action="store_true",
        help="Whether to strip duplicate header includes",
    )
    parser.add_argument(
        "files_or_dirs",
        metavar="FILE_OR_DIR",
        type=str,
        nargs="*",
        help="Files and directories to run this script",
    )
    args = parser.parse_args()
    if not args.files_or_dirs:
        parser.print_help()
        sys.exit(1)

    if (
        not load_quotation_corpus()
        or not load_bracket_corpus()
        or not load_qt_modules()
        or not load_qt_header_mappings()
    ):
        sys.exit(1)

    target_files = []
    target_dirs = []
    for ent in args.files_or_dirs:
        ent = Path(ent)
        if not ent.exists():
            logging.error(f"No-such-file-or-directory: {ent}")
            sys.exit(1)
        if ent.is_file():
            if ent.suffix in C_OR_CPP_EXTENSIONS:
                target_files.append(ent)
            else:
                logging.warn(f"Non-C-family file: {ent}")
        elif ent.is_dir():
            target_dirs.append(ent)
        else:
            logging.error(f"Not-a-regular-file-or-directory: ${ent}")
            sys.exit(1)

    main(target_files, target_dirs, dry=args.dry)
