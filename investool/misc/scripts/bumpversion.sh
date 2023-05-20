#!/bin/bash

# PATHS
PROJECT_PATH=$(dirname $(dirname $(dirname $(realpath $0))))
SRC_PATH=${PROJECT_PATH}/version

VERSION=`git describe --abbrev=0 --tags`

#replace . with space so can split into an array
VERSION_BITS=(${VERSION//./ })

#get number parts and increase last one by 1
VNUM1=${VERSION_BITS[0]}
VNUM2=${VERSION_BITS[1]}
VNUM3=${VERSION_BITS[2]}
VNUM3=$((VNUM3+1))

#create new tag
DEFAULT_TAG="$VNUM1.$VNUM2.$VNUM3"

echo -ne "Updating $VERSION to new tag[${DEFAULT_TAG}]: "
read NEW_TAG
if [ "$NEW_TAG" == "" ]; then
    NEW_TAG=${DEFAULT_TAG}
fi

#get current hash and see if it already has a tag
GIT_COMMIT=`git rev-parse HEAD`
NEEDS_TAG=`git describe --contains $GIT_COMMIT 2>/dev/null`

#only tag if no tag already
if [ -z "$NEEDS_TAG" ]; then
    # https://github.com/x-motemen/gobump
    # 使用 git tag 更新 main.go 中的 VERSION ，去掉前缀 v
    gobump set ${NEW_TAG/#v} -w ${SRC_PATH} && \
    bash ${PROJECT_PATH}/misc/scripts/gen_apidocs.sh && \
    git commit -am "bump verision to $NEW_TAG" && \
    git tag $NEW_TAG && \
    echo "Tagged with $NEW_TAG"
else
    echo "Already a tag on this commit"
fi
