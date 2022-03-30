#!/bin/bash

source get-config.sh

usage()
{
cat << EOF
USAGE: `basename $0` [options]
    -c  config file name
    -w  workflow ID
    -s  status ("-" for reset, "n/a" for not applicable)
EOF
}

while getopts "c:w:s:h" OPTION
do
    case $OPTION in
        c) path_config=$OPTARG ;;
        w) workflow_id=$OPTARG ;;
        s) status=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$workflow_id" ] || [ -z "$status" ] || [ -z "$path_config" ]
then
    usage
    exit 1
fi

server_addr=$(get_config ${path_config} "url")
username=$(get_config ${path_config} "username")
password=$(get_config ${path_config} "password")

curl -X PATCH "${server_addr}/api/workflows/v1/${workflow_id}/labels" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    --data "{\"transfer\":\"$status\"}" \
    --user ${username}:${password} \
    --silent \
    | jq
