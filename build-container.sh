#!/bin/bash

version="0.0.4"

docker build -t cromsfer:${version} .

docker login
docker tag cromsfer:${version} hisplan/cromsfer:${version}
docker push hisplan/cromsfer:${version}
