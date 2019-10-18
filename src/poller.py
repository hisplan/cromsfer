import sys
import os
import argparse
import logging
import time
import subprocess
from pprint import pprint

import auth
import cromwell_interface as client
from redis_queue import RedisQueue


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


def initiate_transfer(path_secrets_file, workflow_id, dry_run):

    cmd = [
        "python", "src/transfer.py",
        f"--secrets={path_secrets_file}",
        f"--workflow-id={workflow_id}"
    ]

    if dry_run:
        cmd.append("--dry-run")

    try:

        subprocess.Popen(cmd)

    except Exception as ex:
        logger.error(ex)


def start_polling(path_secrets_file, polling_time, poll_once, dry_run):

    secrets = auth.get_secrets(path_secrets_file)

    # fixme: get host/port from config file
    queue = RedisQueue(
        name="test",
        host="localhost",
        port=6379
    )

    while True:

        logger.info(
            "Getting the list of completed, but not yet transferred workflows..."
        )

        # get workflows that have been completed successfully but not yet transferred
        data = client.get_succeeded_workflows_not_transferred(secrets)
        # data = client.get_all_workflows(secrets)
        candidates = data["results"]

        if len(candidates) > 0:
            logger.info(
                "Initiating {} output transfer...".format(len(candidates))
            )

        for workflow in candidates:

            workflow_id = workflow["id"]

            logger.info(f"Enqueuing {workflow_id} for output transfer...")

            # initiate_transfer(path_secrets_file, workflow_id, dry_run)
            queue.put(workflow_id)

            client.set_label(
                secrets,
                workflow_id,
                "transfer", "in queue"
            )

        # exit out if poll_once is true
        if poll_once:
            return

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

    parser.add_argument(
        "--once",
        action="store_true",
        dest="poll_once",
        default=False,
        help="Poll only once and exit",
        required=False
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        default=False,
        help="Dry run",
        required=False
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    logger.info("Starting...")

    if params.dry_run:
        logger.info("Running in dry run mode")

    start_polling(
        params.path_secrets_file,
        600,
        params.poll_once,
        params.dry_run
    )

    logger.info("DONE.")
