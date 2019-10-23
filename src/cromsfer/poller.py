import sys
import os
import argparse
import logging
import time
import subprocess
from pprint import pprint

import cromsfer.version as version
import cromsfer.auth as auth
import cromsfer.cromwell_interface as client
from cromsfer.redis_queue import RedisQueue


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


def start_polling(path_config, polling_time, poll_once, dry_run):

    config = auth.get_config(path_config)

    # fixme: get host/port from config file
    queue = RedisQueue(
        name="cromsfer",
        host=config["redis"]["host"],
        port=config["redis"]["port"]
    )

    while True:

        logger.info(
            "Getting the list of completed, but not yet transferred workflows..."
        )

        # get workflows that have been completed successfully but not yet transferred
        data = client.get_succeeded_workflows_not_transferred(
            config["cromwell"]
        )

        candidates = data["results"]

        if len(candidates) > 0:
            logger.info(
                "Initiating {} output transfer...".format(len(candidates))
            )
        else:
            logger.info("No work to do...")

        for workflow in candidates:

            workflow_id = workflow["id"]

            logger.info(f"Enqueuing {workflow_id} for output transfer...")

            queue.put(workflow_id)

            client.set_label(
                config["cromwell"],
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
        "-c", "--config",
        action="store",
        dest="path_config",
        default="config.yaml",
        help="path to configuration file",
        required=False
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

    parser.add_argument(
        "-v", "--version",
        action="version",
        version='cromsfer.{} v{}'.format(parser.prog, version.__version__)
    )

    # parse arguments
    params = parser.parse_args()

    return params


def main():

    params = parse_arguments()

    logger.info("Starting...")

    if params.dry_run:
        logger.info("Running in dry run mode")

    start_polling(
        params.path_config,
        600,
        params.poll_once,
        params.dry_run
    )

    logger.info("DONE.")


if __name__ == "__main__":
    main()
