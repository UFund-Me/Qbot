#!/bin/bash

set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd -P)"


CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -ldflags "-X github.com/axiaoxin-com/investool/version.Version=`TZ=Asia/Shanghai date +'%y%m%d%H%M'`" -o investool_app_mac
sed -i "s/env = \"localhost\"/env = \"prod\"/g" config.toml && tar czvf investool_app_mac.tar.gz investool_app_mac config.toml

