#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # outCBSortedTaggedBam
    # "s3://dp-lab-batch/cromwell-execution/Velopipe2/f8622453-33a1-428b-8eb1-b24c1800214f/call-CBSortedTaggedBam/cellsorted_MPL_CD40.tagged.bam"

    # outLoom
    # "s3://dp-lab-batch/cromwell-execution/Velopipe2/f8622453-33a1-428b-8eb1-b24c1800214f/call-Velocyto/glob-6e284a9cd30ed4548d4059bf33133003/MPL_CD40_IL001.loom"

    # outPosSortedTaggedBai
    # "s3://dp-lab-batch/cromwell-execution/Velopipe2/f8622453-33a1-428b-8eb1-b24c1800214f/call-MergeBam/MPL_CD40.tagged.bai"

    # outPosSortedTaggedBam
    # "s3://dp-lab-batch/cromwell-execution/Velopipe2/f8622453-33a1-428b-8eb1-b24c1800214f/call-MergeBam/MPL_CD40.tagged.bam"

    # outTagBamLog
    # "s3://dp-lab-batch/cromwell-execution/Velopipe2/f8622453-33a1-428b-8eb1-b24c1800214f/call-TagBam2/tag_bam.log"

    items = list()

    items.append(
        (outputs["Velopipe.outLoom"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe.outCBSortedTaggedBam"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe.outPosSortedTaggedBam"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe.outPosSortedTaggedBai"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe.outTagBamLog"], base_destination + "/")
    )

    items.append(
        (outputs["Velopipe.outVelocytoLog"], base_destination + "/")
    )

    return items
