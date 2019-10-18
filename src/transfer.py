import os
import sys
import subprocess
import logging
import argparse
import json
from pprint import pprint

import auth
import cromwell_interface as client
from redis_queue import RedisQueue


logger = logging.getLogger("transfer")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("transfer.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def run_command(cmd):
    "run a command and return (stdout, stderr, exit code)"

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False
    )

    for line in iter(process.stdout.readline, b''):
        line = line.decode(sys.stdout.encoding).rstrip() + "\r"
        logger.info(line)


def copy_gcp(src, dst, dry_run):

    if dry_run:
        return

    run_command(
        ["gsutil", "cp", src, dst]
    )


def copy_aws(src, dst, dry_run):

    if dry_run:
        return

    run_command(
        ["aws", "s3", "cp", src, dst]
    )


def write_metadata(workflow_id, metadata, path_tmp):

    os.makedirs(path_tmp, exist_ok=True)

    path_metadata = os.path.join(
        path_tmp, f"{workflow_id}-metadata.json"
    )

    with open(path_metadata, "wt") as fout:
        fout.write(
            json.dumps(metadata, indent=2)
        )

    return path_metadata


def transfer(path_secrets_file, workflow_id, path_tmp, dry_run):

    # fixme: determine aws or gcp
    copy = copy_gcp

    secrets = auth.get_secrets(path_secrets_file)

    try:
        logger.info(f"{workflow_id}: getting the metadata...")

        metadata = client.get_metadata(secrets, workflow_id)

        outputs = metadata["outputs"]
        pipeline_type = metadata["labels"]["pipelineType"]
        base_destination = metadata["labels"]["destination"].rstrip("/")
        transfer_status = metadata["labels"]["transfer"]

        logger.info(
            f"{workflow_id}: current transfer status = {transfer_status}"
        )

        if transfer_status == "in queue":
            client.set_label(
                secrets,
                workflow_id,
                "transfer", "initiated"
            )
        else:
            logger.info(
                f"{workflow_id}: Aborting due to the current transfer status = {transfer_status}"
            )
            return

        path_metadata = write_metadata(workflow_id, metadata, path_tmp)

        logger.info(
            f"{workflow_id}: transferring the metadata to {base_destination}"
        )

        copy(path_metadata, base_destination + "/", dry_run)

        # fixme: refactor later
        if pipeline_type == "Test":
            from workflows import Test as x
            construct_src_dst_info = x.construct_src_dst_info
        elif pipeline_type == "Sharp":
            from workflows import Sharp as x
            construct_src_dst_info = x.construct_src_dst_info
        elif pipeline_type == "Velopipe":
            from workflows import Velopipe as x
            construct_src_dst_info = x.construct_src_dst_info
        else:
            raise Exception("Unknown pipeline type")

        items = construct_src_dst_info(workflow_id, outputs, base_destination)

        if items:
            for (src, dst) in items:
                logger.info(f"{workflow_id}: transferring from {src} to {dst}")
                copy(src, dst, dry_run)
        else:
            logger.info(f"{workflow_id}: nothing to transfer")

        client.set_label(
            secrets,
            workflow_id,
            "transfer", "done"
        )

    except Exception as ex:
        logger.error(f"{workflow_id}: " + str(ex))

        client.set_label(
            secrets,
            workflow_id,
            "transfer", "failed"
        )


def dequeue(path_secrets_file, workflow_id, path_tmp, poll_once, dry_run):

    # fixme: get host/port from config file
    queue = RedisQueue(
        name="test",
        host="localhost",
        port=6379
    )

    while True:

        logger.info(
            "Waiting for a new task..."
        )

        workflow_id = queue.get(block=True, timeout=None)
        workflow_id = workflow_id.decode()

        logger.info(
            f"{workflow_id}: Dequeued"
        )

        transfer(
            path_secrets_file,
            workflow_id,
            path_tmp,
            dry_run
        )

        # exit out if poll_once is true
        if poll_once:
            return


def main(path_secrets_file, workflow_id, path_tmp, poll_once, dry_run):

    if workflow_id:

        transfer(
            path_secrets_file,
            workflow_id,
            path_tmp,
            dry_run
        )

    else:

        dequeue(
            path_secrets_file,
            workflow_id,
            path_tmp,
            poll_once,
            dry_run
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

    parser.add_argument(
        "--workflow-id",
        action="store",
        dest="workflow_id",
        default=None,
        help="Workflow ID",
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
        "--once",
        action="store_true",
        dest="poll_once",
        default=False,
        help="Poll only once and exit",
        required=False
    )

    parser.add_argument(
        "--tmp",
        action="store",
        dest="path_tmp",
        help="path to temporary directory",
        default="./tmp",
        required=False
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    logger.info(f"Starting...")

    if params.dry_run:
        logger.info("Running in dry run mode")

    main(
        params.path_secrets_file,
        params.workflow_id,
        params.path_tmp,
        params.poll_once,
        params.dry_run
    )

    logger.info("DONE.")
