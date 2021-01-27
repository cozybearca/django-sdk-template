#!/bin/bash

# use this bash script to launch and login to sdk container
__dir__="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export HOST_SDK_ROOT="$__dir__/.."

export PROJ_NAME="testrepo"
export HOST_PORT_SPACE="2"
export GIT_USER="ylilarry@gmail.com"
export GIT_REGISTRY_TOKEN="0149e0660e38b8704a10ab5c7f1ccc1446dca82d"
export SDK_IMAGE_PREFIX="docker.pkg.github.com/cozybearca/${PROJ_NAME}/"
export SDK_TAG=1 # sdk version

export COMPOSE_PROJECT_NAME="${PROJ_NAME}"
