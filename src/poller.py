import sys
import os
import argparse
import logging
import time
from pprint import pprint

import auth
import cromwell_interface as client


logger = logging.getLogger("poller")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("poller.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def initiate_transfer(path_secrets_file, workflow_id):

    try:
        os.system(
            f"python src/transfer.py --secrets={path_secrets_file} --workflow-id={workflow_id}"
        )

    except Exception as ex:
        logger.error(ex)


def start_polling(path_secrets_file, polling_time):

    secrets = auth.get_secrets(path_secrets_file)

    while True:

        logger.info(
            "Getting the list of completed, but not yet transferred workflows...")

        # get workflows that have been completed successfully but not yet transferred
        data = client.get_succeeded_workflows_not_transferred(secrets)
        # data = client.get_all_workflows(secrets)
        candidates = data["results"]

        if len(candidates) > 0:
            logger.info("Initiating {} output transfer...".format(len(candidates)))

        for workflow in candidates:

            workflow_id = workflow["id"]

            client.set_label(
                secrets,
                workflow_id,
                "transfer", "initiated"
            )

            logger.info(f"Transfer initiated for {workflow_id}")

            initiate_transfer(path_secrets_file, workflow_id)

        time.sleep(polling_time)


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

    start_polling(
        params.path_secrets_file,
        600
    )
