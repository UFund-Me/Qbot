#! /usr/bin/env bash
# 编译并docker中运行

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

PROJECT_PATH=$(dirname $(dirname $(dirname $(realpath $0))))

source ${PROJECT_PATH}/misc/scripts/dist.sh

docker build -t investool ${PROJECT_PATH}
docker run -p 4869:4869 -p 4870:4870 investool
