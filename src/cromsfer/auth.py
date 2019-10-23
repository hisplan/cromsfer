#!/usr/bin/env python
import json
import yaml

def get_secrets(path_secrets_file):

    with open(path_secrets_file, "rt") as fin:
        data = json.loads(fin.read())

    return data


def get_config(path_config):

    with open(path_config, "rt") as fin:
        data = yaml.load(fin, Loader=yaml.FullLoader)

    return data
