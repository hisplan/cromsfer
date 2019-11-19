FROM ubuntu:18.04

LABEL maintainer="Jaeyoung Chun (chunj@mskcc.org)"

ENV CROMSFER_VERSION 0.0.7

RUN apt-get update \
    && apt-get install --yes build-essential python3 python3-pip

RUN apt-get install --yes wget zlib1g-dev libbz2-dev liblzma-dev

COPY tmp/cromsfer-${CROMSFER_VERSION}.tar.gz /tmp/

# for private
RUN cd /tmp \
    && tar xvzf cromsfer-${CROMSFER_VERSION}.tar.gz \
    && cd cromsfer-${CROMSFER_VERSION} \
    && pip3 install .

# for public
# RUN cd /tmp \
#     && wget https://github.com/hisplan/cromsfer/releases/tag/v${CROMSFER_VERSION} \
#     && tar xvzf v${CROMSFER_VERSION}.tar.gz \
#     && cd cromsfer-v${CROMSFER_VERSION} \
#     && pip3 install .

RUN pip3 install awscli

# install gsutil
