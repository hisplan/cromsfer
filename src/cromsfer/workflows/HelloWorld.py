#!/usr/bin/env python

def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "HelloWorld.outString": "Hello, World! Jaeyoung",
    #   "HelloWorld.outFile": "s3://dp-lab-gwf-core/cromwell-execution/HelloWorld/42288e23-70a6-43b6-91e5-d33bad20beac/call-SayToFile/hello.txt"
    # }

    items = list()

    items.append(
        (outputs["HelloWorld.outFile"], base_destination + "/")
    )

    return items
