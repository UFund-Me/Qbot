#! /usr/bin/env bash
# 编译打包二进制文件

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

# PATHS
PROJECT_PATH=$(dirname $(dirname $(dirname $(realpath $0))))
SRC_PATH=${PROJECT_PATH}
DIST_PATH=${PROJECT_PATH}/dist
NOW=$(date "+%Y%m%d-%H%M%S")


# ERROR CODE
TESTING_FAILED=-1
BUILDING_FAILED=-2

# vars
BINARY_NAME=apiserver
CONFIGFILE=config.default.toml
TARNAME=investool

# clean dist dir
clean() {
    rm -rf ${DIST_PATH}
}

# running go test
tests() {
    # Running tests
    echo -e "Running tests"
    cd ${SRC_PATH}
    if !(go test -race ./...)
    then
        echo -e "Tests failed."
        cd -
        exit ${TESTING_FAILED}
    fi
    cd -
}

# gen apidocs and go build
build() {
    echo -ne "Enter release binary name [${BINARY_NAME}]: "
    read binary_name
    if [ "${binary_name}" != "" ]; then
        BINARY_NAME=${binary_name}
    fi

    echo -e "Will build binary name to be ${BINARY_NAME}"

    # Update docs
    echo "Updating swag docs"
    # check swag
    if !(swag > /dev/null 2>&1); then
        echo -e "Need swag to generate API docs. Installing swag..."
        go get -u github.com/swaggo/swag/cmd/swag
    fi
    echo -e "Generating API docs..."
    bash ${PROJECT_PATH}/misc/scripts/gen_apidocs.sh

    # Building
    echo -e "Building..."
    if [ ! -d ${DIST_PATH} ]; then
        mkdir ${DIST_PATH}
    fi
    cd ${SRC_PATH}
    GOOS=linux GOARCH=amd64 go build -o ${DIST_PATH}/${BINARY_NAME} ${SRC_PATH}
    if [ $? -ne 0 ]
    then
        echo -e "Build failed."
        exit ${BUILDING_FAILED}
    fi
    cd -
}

# tar bin and config file
tarball() {
    echo -ne "Enter your configfile[${CONFIGFILE}]: "
    read cf
    if [ "${cf}" != "" ]; then
        CONFIGFILE=${cf}
    fi

    echo -e "tar binary file and config file..."
    tardir=${DIST_PATH}/${TARNAME}
    mkdir ${tardir}
    mv ${DIST_PATH}/${BINARY_NAME} ${tardir}
    cp ${SRC_PATH}/${CONFIGFILE} ${tardir}
    tar czvf ${tardir}.tar.gz -C ${DIST_PATH} ${TARNAME} && rm -rf ${tardir}
}

main() {
    echo -e "This tool will help you to release your app.\nIt will run tests then update apidocs and build the binary file and tar it with configfile as tar.gz file."
    clean
    tests
    build
    tarball
}

main
