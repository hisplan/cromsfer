#!/bin/bash

source get-config.sh

usage()
{
cat << EOF
USAGE: `basename $0` [options]
    -c  config file name
    -w  workflow ID
EOF
}

while getopts "c:w:h" OPTION
do
    case $OPTION in
        c) path_config=$OPTARG ;;
        w) workflow_id=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$workflow_id" ] || [ -z "$path_config" ]
then
    usage
    exit 1
fi

server_addr=$(get_config ${path_config} "url")
username=$(get_config ${path_config} "username")
password=$(get_config ${path_config} "password")

curl -X GET "${server_addr}/api/workflows/v1/${workflow_id}/metadata?expandSubWorkflows=false" \
    -H "accept: application/json" \
    --user ${username}:${password} \
    --silent \
    | jq
