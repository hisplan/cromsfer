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

server_addr="ec2-100-26-88-232.compute-1.amazonaws.com"

usage()
{
cat << EOF
USAGE: `basename $0` [options]
    -w  workflow ID
EOF
}

while getopts "w:h" OPTION
do
    case $OPTION in
        w) workflow_id=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$workflow_id" ]
then
    usage
    exit 1
fi

curl -X GET "http://ec2-100-26-88-232.compute-1.amazonaws.com/api/workflows/v1/${workflow_id}/metadata?expandSubWorkflows=false" \
    -H "accept: application/json" \
    --user ${JOB_MANAGER_USERNAME}:${JOB_MANAGER_PWD} \
    --silent \
    | jq
