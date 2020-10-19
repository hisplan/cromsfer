#!/bin/bash

if [ -z "$JOB_MANAGER_USERNAME" ] || [ -z "$JOB_MANAGER_PWD" ]
then
    echo "Credentials required!"
    echo
    echo "export JOB_MANAGER_USERNAME=<put-your-username-here>"
    echo "export JOB_MANAGER_PWD=<put-your-password-here>"
    echo
    exit 1
fi

if [ -z $1 ]
then
  echo "Specify a workflow ID."
  exit 1
fi

./transfer-status.sh -w $1 -s n/a
