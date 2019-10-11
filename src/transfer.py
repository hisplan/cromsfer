import os
import sys
import subprocess
import logging
import argparse
import json
from pprint import pprint

import auth
import cromwell_interface as client


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


def copy_gcp(src, dst):

    run_command(
        ["gsutil", "cp", src, dst]
    )


def copy_aws(src, dst):

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


def transfer(path_secrets_file, workflow_id, path_tmp):

    # fixme: determine aws or gcp
    copy = copy_gcp

    secrets = auth.get_secrets(path_secrets_file)

    try:
        logger.info(f"{workflow_id}: getting the metadata...")

        metadata = client.get_metadata(secrets, workflow_id)

        outputs = metadata["outputs"]
        pipeline_type = metadata["labels"]["pipelineType"]
        base_destination = metadata["labels"]["destination"].rstrip("/")

        path_metadata = write_metadata(workflow_id, metadata, path_tmp)

        logger.info(
            f"{workflow_id}: transferring the metadata to {base_destination}")

        copy(path_metadata, base_destination + "/")

        # fixme: refactor later
        if pipeline_type == "Test":
            from workflows import Test as x
            construct_src_dst_info = x.construct_src_dst_info
        elif pipeline_type == "Sharp":
            from workflows import Sharp as x
            construct_src_dst_info = x.construct_src_dst_info
        else:
            raise Exception("Unknown pipeline type")

        items = construct_src_dst_info(workflow_id, outputs, base_destination)

        if items:
            for (src, dst) in items:

                logger.info(f"{workflow_id}: transferring from {src} to {dst}")
                copy(src, dst)
        else:
            logger.info(f"{workflow_id}: nothing to transfer")

    except Exception as ex:
        logger.error(f"{workflow_id}: " + ex)


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
        help="Workflow ID",
        required=True
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

    logger.info(f"{params.workflow_id}: Starting...")

    transfer(
        params.path_secrets_file,
        params.workflow_id,
        params.path_tmp
    )

    logger.info(f"{params.workflow_id}: DONE.")
