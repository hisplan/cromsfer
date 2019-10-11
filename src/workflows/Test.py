#!/usr/bin/env python

def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #     'Main.outFile': 'gs://chunj-cromwell/cromwell-execution/Main/c4e1d18a-01ee-4ed0-be3b-2ae9f78f4a63/call-SayToFile/hello.txt',
    #     'Main.outString': 'Hello, World! Jaeyoung'
    # }

    items = list()

    items.append(
        (outputs["Main.outFile"], base_destination + "/")
    )

    return items
