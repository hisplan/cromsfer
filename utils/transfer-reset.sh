#!/bin/bash

if [ -z $1 ]
then
  echo "Specify a workflow ID."
  exit 1
fi

./transfer-status.sh -w $1 -s -
