#!/bin/sh

find . -name "*.py" -or -name "config.py-example" | xargs black --line-length 100
