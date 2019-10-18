# cromwell-output-transfer

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
