#!/bin/bash

version="0.0.6"

docker build -t cromsfer:${version} .

docker login
docker tag cromsfer:${version} hisplan/cromsfer:${version}
docker push hisplan/cromsfer:${version}
