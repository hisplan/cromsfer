# cromsfer

Cromwell Output Transfer

## Prerequisites

- AWS CLI
- gsutil

## Redis

```bash
$ docker run --rm -d -p 6379:6379 redis:5.0.6
```

## Poller

`cromsfer.poller` picks up the workflows that have been completed, but not yet transferred.

```bash
$ cromsfer.poller
```

## Transfer

```bash
$ cromsfer.transfer
```

## Development

```bash
$ conda create -n cromsfer python=3.6.5 pip
$ conda activate cromsfer
$ git clone ...
$ pip install -e .
```
