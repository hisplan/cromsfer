import sys
import os
import argparse
import json
import time
import subprocess
from pprint import pprint

import auth
import cromwell_interface as client


def write(data, filename):

    path_base = "test/data"
    os.makedirs(path_base, exist_ok=True)

    print(filename)

    with open(os.path.join(path_base, filename), "wt") as fout:
        fout.write(
            json.dumps(data, indent=2)
        )


def dump(path_secrets_file):

    secrets = auth.get_secrets(path_secrets_file)

    data = client.get_all_workflows(secrets)

    write(data, "all-workflows.json")

    candidates = data["results"]

    for workflow in candidates:

        workflow_id = workflow["id"]

        metadata = client.get_metadata(secrets, workflow_id)

        write(metadata, f"{workflow_id}-metadata.json")


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--secrets",
        action="store",
        dest="path_secrets_file",
        help="path to secrets file",
        required=True
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    dump(
        params.path_secrets_file
    )
