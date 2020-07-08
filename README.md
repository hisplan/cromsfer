# Cromwell Output Transfer (Cromsfer)

Transfers output files from Cromwell/WDL workflows to a designated S3 locations with a human-friendly directory structure. It supports:

- FastQC (FASTQ QC)
- SeqcCustomGenes (Custom Genes/Reporter Genes)
- Sharp (Hashtag)
- Velopipe (RNA Velocity)

## Prerequisites

- AWS CLI
- gsutil

## Development Environment

### Install Cromsfer

```bash
$ conda create -n cromsfer python=3.7.6 pip
$ conda activate cromsfer
$ git clone ...
$ pip install -e .
```

### Run Redis

```bash
$ docker run --rm -d -p 6379:6379 redis:5.0.6
```

### Run the Poller Service

`cromsfer.poller` picks up the workflows that have been completed, but not yet transferred.

```bash
$ cromsfer.poller --config config.aws-local-redis.yaml
```

### Run the Transfer Service

```bash
$ cromsfer.transfer  --config config.aws-local-redis.yaml
```

### Utilities

```bash
$ export JOB_MANAGER_USERNAME=johnDoe
$ export JOB_MANAGER_PWD=xyz123abc
```

```bash
$ cd utils
$ ./get-metadata.sh
```