# Cromwell Output Transfer (Cromsfer)

Transfers output files from Cromwell/WDL workflows to a designated S3 locations with a human-friendly directory structure. It supports:

- FastQC (FASTQ QC)
- STAR Transgenes
- Sharp (Hashtag and CellPlex)
- Sharp (CITE-seq)
- Sharp (ASAP-seq)
- Velopipe (RNA Velocity)
- Cell Ranger V(D)J
- Cell Ranger GEX
- Cell Ranger ATAC
- Cell Ranger ARC
- Cell Ranger CellPlex
- ArchR Stand Alone (aka. ArchRSA)
- mkref (Generating genome index for STAR aligner)

## Prerequisites

- AWS CLI
- gsutil

## Development Environment

### Install Cromsfer

```bash
conda create -n cromsfer python=3.8 pip
conda activate cromsfer
git clone https://github.com/hisplan/cromsfer.git
pip install -e .[dev]
```

### Run Redis

```bash
docker run --rm -d -p 6379:6379 redis:5.0.6
```

### Run the Poller Service

`cromsfer.poller` picks up the workflows that have been completed, but not yet transferred.

```bash
cromsfer.poller --config config.aws-local-redis.yaml
```

### Run the Transfer Service

```bash
cromsfer.transfer  --config config.aws-local-redis.yaml
```

### Utilities

```bash
$ export JOB_MANAGER_USERNAME=johnDoe
$ export JOB_MANAGER_PWD=xyz123abc
```

Getting the metadata for a given workflow:

```bash
$ cd utils
$ ./get-metadata.sh -w 4bb895a2-dc44-4d6d-94ca-1294452e1bf8
```

Resetting the transfer status (i.e. "`-`")

```bash
$ cd utils
$ ./transfer-reset.sh -w 4bb895a2-dc44-4d6d-94ca-1294452e1bf8
```

## Deployment

1. Make sure you increment the version number (`src/cromsfer/version.py`).
1. Push all the changes into the GitHub repository.
1. Create a release tag in the GitHub repository.
1. Build a docker image.
