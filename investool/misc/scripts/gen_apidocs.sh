#! /usr/bin/env bash
# 生成swag api文档

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

PROJECT_PATH=$(dirname $(dirname $(dirname $(realpath $0))))
SRC_PATH=${PROJECT_PATH}

# swag init必须在main.go所在的目录下执行，否则必须用--dir参数指定main.go的路径
# go get -u github.com/swaggo/swag/cmd/swag
swag init --dir ${SRC_PATH}/ --generalInfo routes/routes.go --propertyStrategy snakecase --output ${SRC_PATH}/routes/docs
