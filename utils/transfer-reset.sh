#!/bin/bash

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

./transfer-status.sh \
  -c ${path_config} \
  -w ${workflow_id} \
  -s -
