#!/bin/bash -e

# if [ -z ${GIT_AUTH_TOKEN} ]
# then
#     echo "GIT_AUTH_TOKEN must be set in order to download Cromsfer from the private repository."
#     exit 1
# fi

version=`python -c "exec(open('src/cromsfer/version.py').read()); print(__version__)"`

docker build \
    --build-arg GIT_AUTH_TOKEN=${GIT_AUTH_TOKEN} \
    --build-arg CROMSFER_VERSION=${version} \
    -t cromsfer:${version} .

docker login
docker tag cromsfer:${version} hisplan/cromsfer:${version}
docker push hisplan/cromsfer:${version}
