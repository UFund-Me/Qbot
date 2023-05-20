#!/bin/bash
# git tag first
echo "release..."
goreleaser release --rm-dist
