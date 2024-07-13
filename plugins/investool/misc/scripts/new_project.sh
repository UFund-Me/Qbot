#! /usr/bin/env bash

main() {
    gopath=`go env GOPATH`
    if [ $? = 127 ]; then
        echo "GOPATH not exists"
        exit -1
    fi
    echo -e "New project will be create in ${gopath}/src/"
    echo -ne "Enter your new project full name: "
    read projname

    # get template project
    echo -e "Downloading the template..."
    # git clone https://github.com/axiaoxin-com/pink-lady.git ${gopath}/src/${projname}
    rm -
    if !(curl https://codeload.github.com/axiaoxin-com/pink-lady/zip/master -o /tmp/pink-lady.zip && unzip /tmp/pink-lady.zip -d /tmp)
    then
        echo "Downloading failed."
        exit -2
    fi

    echo -e "Generating the project..."
    mv /tmp/pink-lady-master ${gopath}/src/${projname} && cd ${gopath}/src/${projname}

    if [ `uname` = 'Darwin' ]; then
        sed -i '' -e "s|github.com/axiaoxin-com/pink-lady|${projname}|g" `grep "pink-lady" --include "swagger.*" --include ".travis.yml" --include "*.go" --include "go.*" -rl .`
    else
        sed -i "s|github.com/axiaoxin-com/pink-lady|${projname}|g" `grep "pink-lady" --include "swagger.*" --include ".travis.yml" --include "*.go" --include "go.*" -rl .`
    fi

    if [ $? -ne 0 ]
    then
        echo -e "set project name failed."
        exit -3
    fi

    echo -e "Create project ${projname} in ${gopath}/src succeed."

    # init a git repo
    echo -ne "Do you want to init a git repo[N/y]: "
    read initgit
    if [ "${initgit}" == "y" ] || [ "${rmdemo}" == "Y" ]; then
        cd ${gopath}/src/${projname} && git init && git add . && git commit -m "init project with pink-lady"
        cp ${gopath}/src/${projname}/misc/scripts/pre-push.githook ${gopath}/src/${projname}/.git/hooks/pre-push
        chmod +x ${gopath}/src/${projname}/.git/hooks/pre-push
    fi
}
main
