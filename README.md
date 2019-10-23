# cromsfer

Cromwell Output Transfer

## Prerequisites

- AWS CLI
- gsutil

## Redis

```bash
$ docker run --rm  -d -p 6379:6379 redis:5.0.6
```

## Poller

`poller.py` picks up the workflows that have been completed, but 

```bash
$ python poller.py --secrets=~/secrets-gcp.json
```

## Transfer

```bash
$ python transfer.py --secrets=~/secrets-gcp.json
```

## Dev

```bash
$ conda create -n cromsfer python=3.6.5 pip
$ conda activate cromsfer
$ git clone ...
$ pip install -e .
```
