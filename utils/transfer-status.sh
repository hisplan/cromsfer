#!/bin/bash

if [ -z "$JOB_MANAGER_USERNAME" ] || [ -z "$JOB_MANAGER_PWD" ]
then
    echo "JOB_MANAGER_USERNAME and/or JOB_MANAGER_PWD are not configured!"
    exit 1
fi

server_addr="ec2-100-26-88-232.compute-1.amazonaws.com"

usage()
{
cat << EOF
USAGE: `basename $0` [options]
    -w  workflow ID
    -s  status ("-" for reset, "n/a" for not applicable)
EOF
}

while getopts "w:s:h" OPTION
do
    case $OPTION in
        w) workflow_id=$OPTARG ;;
        s) status=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$workflow_id" ] || [ -z "$status" ]
then
    usage
    exit 1
fi

curl -X PATCH "http://${server_addr}/api/workflows/v1/${workflow_id}/labels" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    --data "{\"transfer\":\"$status\"}" \
    --user ${JOB_MANAGER_USERNAME}:${JOB_MANAGER_PWD} \
    --silent \
    | jq
