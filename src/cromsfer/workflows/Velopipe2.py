#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # "Velopipe2.outVelocytoLog": "s3://dp-lab-batch/cromwell-execution/Velopipe2/4bb895a2-dc44-4d6d-94ca-1294452e1bf8/call-Velocyto/velocyto.log",
    # "Velopipe2.outLoom": "s3://dp-lab-batch/cromwell-execution/Velopipe2/4bb895a2-dc44-4d6d-94ca-1294452e1bf8/call-Velocyto/glob-6e284a9cd30ed4548d4059bf33133003/RU263_DZ0L6.loom",
    # "Velopipe2.outPosSortedTaggedBam": "s3://dp-lab-batch/cromwell-execution/Velopipe2/4bb895a2-dc44-4d6d-94ca-1294452e1bf8/call-MergeBam/RU263.tagged.bam",
    # "Velopipe2.outTagBamLog": "s3://dp-lab-batch/cromwell-execution/Velopipe2/4bb895a2-dc44-4d6d-94ca-1294452e1bf8/call-TagBam2/tag_bam.log",
    # "Velopipe2.outCBSortedTaggedBam": "s3://dp-lab-batch/cromwell-execution/Velopipe2/4bb895a2-dc44-4d6d-94ca-1294452e1bf8/call-CBSortedTaggedBam/cellsorted_RU263.tagged.bam",
    # "Velopipe2.outPosSortedTaggedBai": "s3://dp-lab-batch/cromwell-execution/Velopipe2/4bb895a2-dc44-4d6d-94ca-1294452e1bf8/call-MergeBam/RU263.tagged.bai"

    items = list()

    items.append(
        (outputs["Velopipe2.outLoom"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe2.outCBSortedTaggedBam"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe2.outPosSortedTaggedBam"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe2.outPosSortedTaggedBai"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe2.outTagBamLog"], base_destination + "/")
    )

    # hack: the v2-beta pipeline might not have Velopipe2.outVelocytoLog.
    # let's skip in that case.
    if "Velopipe2.outVelocytoLog" in outputs:
        items.append(
            (outputs["Velopipe2.outVelocytoLog"], base_destination + "/")
        )

    return items
