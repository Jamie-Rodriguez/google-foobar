#!/usr/bin/env bash
# IMPORTANT: Run me from the root directory (not inside the target directory)!
set -euo pipefail

if [[ $# -eq 0 ]] ; then
    echo 'Error: no target directory provided!'
    exit 1
fi

if [[ ! -d $1 ]] ; then
    echo "Error: Directory \"$1\" does not exist!"
    exit 1
fi

# As all problems have the same structure,
# should only need to change the directory to 'cd' into:
cd $1

docker run --interactive \
    --tty \
    --rm \
    --name google-foobar-solution \
    --volume "$PWD":/usr/src/google-foobar \
    --workdir /usr/src/google-foobar \
    openjdk:8u322-jdk /bin/bash -c "javac Solution.java && java Solution"
