#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #     'Velopipe.outLoom': 'gs://chunj-cromwell/cromwell-execution/Velopipe/790766eb-1979-4e5a-8124-f1dbce445b2e/call-Velocyto/glob-6e284a9cd30ed4548d4059bf33133003/sampled_679SW.loom',
    #     'Velopipe.outBai': 'gs://chunj-cromwell/cromwell-execution/Velopipe/790766eb-1979-4e5a-8124-f1dbce445b2e/call-SortIndexTaggedBam/sampled.tagged.sorted.bam.bai',
    #     'Velopipe.outBam': 'gs://chunj-cromwell/cromwell-execution/Velopipe/790766eb-1979-4e5a-8124-f1dbce445b2e/call-SortIndexTaggedBam/sampled.tagged.sorted.bam'
    # }

    items = list()

    items.append(
        (outputs["Velopipe.outLoom"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe.outBam"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe.outBai"], base_destination + "/")
    )

    return items
