#!/bin/bash -e

if [ -z ${GIT_AUTH_TOKEN} ]
then
    echo "GIT_AUTH_TOKEN must be set in order to download ArchR from the private repository."
    exit 1
fi

version="0.0.20"

docker build --build-arg GIT_AUTH_TOKEN -t cromsfer:${version} .

docker login
docker tag cromsfer:${version} hisplan/cromsfer:${version}
docker push hisplan/cromsfer:${version}
