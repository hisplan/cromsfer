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
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("cromsfer.poller.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def start_polling(path_config, poll_interval, poll_once, dry_run):

    config = auth.get_config(path_config)

    # fixme: get host/port from config file
    queue = RedisQueue(
        name="cromsfer",
        host=config["redis"]["host"],
        port=config["redis"]["port"]
    )

    while True:

        logger.info(
            "Waiting for a new task..."
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

            queue.put(workflow_id)

            logger.info(f"{workflow_id} queued for output transfer...")

            client.set_label(
                config["cromwell"],
                workflow_id,
                "transfer", "in queue"
            )

        # exit out if poll_once is true
        if poll_once:
            return

        time.sleep(poll_interval)


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
        "--interval",
        action="store",
        type=int,
        dest="poll_interval",
        default=600,
        help="poll interval in seconds",
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
        params.poll_interval,
        params.poll_once,
        params.dry_run
    )

    logger.info("DONE.")


if __name__ == "__main__":
    main()
