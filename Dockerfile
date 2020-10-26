FROM ubuntu:18.04

LABEL maintainer="Jaeyoung Chun (chunj@mskcc.org)"

ARG GIT_AUTH_TOKEN
ENV CROMSFER_VERSION 0.0.16

RUN apt-get update \
    && apt-get install --yes build-essential python3 python3-pip

RUN apt-get install --yes wget curl zlib1g-dev libbz2-dev liblzma-dev

# for private repo
RUN cd /tmp \
    && curl -L -o cromsfer.tgz -H "Authorization: token ${GIT_AUTH_TOKEN}" https://github.com/hisplan/cromsfer/archive/v${CROMSFER_VERSION}.tar.gz \
    && tar xvzf cromsfer.tgz \
    && cd cromsfer-${CROMSFER_VERSION} \
    && pip3 install .

# for public repo
# RUN cd /tmp \
#     && wget https://github.com/hisplan/cromsfer/releases/tag/v${CROMSFER_VERSION} \
#     && tar xvzf v${CROMSFER_VERSION}.tar.gz \
#     && cd cromsfer-v${CROMSFER_VERSION} \
#     && pip3 install .

RUN pip3 install awscli

# install gsutil
