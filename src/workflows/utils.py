import sys
import subprocess


def run_command(cmd, logger):
    "run a command and return (stdout, stderr, exit code)"

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False
    )

    for line in iter(process.stdout.readline, b''):
        line = line.decode(sys.stdout.encoding).rstrip() + "\r"
        logger.info(line)
