import sys
import os
import argparse
import logging
import time
from pprint import pprint

import auth
import cromwell_interface as client


def main(path_secrets_file):

    secrets = auth.get_secrets(path_secrets_file)

    data = client.get_all_workflows(secrets)
    candidates = data["results"]

    for workflow in candidates:

        workflow_id = workflow["id"]

        print(workflow_id)

        client.set_label(
            secrets,
            workflow_id,
            "transfer", ""
        )


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

    main(
        params.path_secrets_file
    )
