#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # outLoom
    # "s3://dp-lab-batch/cromwell-execution/Velopipe/8b57436f-b4eb-4341-9af1-5b9567b40170/call-Velocyto/glob-6e284a9cd30ed4548d4059bf33133003/1380_IL10R_P176_IGO_10084_4_Aligned_DOPRI.loom"

    # outCBSortedTaggedBam
    # "s3://dp-lab-batch/cromwell-execution/Velopipe/8b57436f-b4eb-4341-9af1-5b9567b40170/call-CBSortedTaggedBam/cellsorted_1380_IL10R_P176_IGO_10084_4_Aligned.out.sorted.tagged.bam"

    # outPosSortedTaggedBam
    # "s3://dp-lab-batch/cromwell-execution/Velopipe/8b57436f-b4eb-4341-9af1-5b9567b40170/call-PosSortedTaggedBam/1380_IL10R_P176_IGO_10084_4_Aligned.out.sorted.tagged.sorted.bam"

    # outPosSortedTaggedBai
    # "s3://dp-lab-batch/cromwell-execution/Velopipe/8b57436f-b4eb-4341-9af1-5b9567b40170/call-PosSortedTaggedBam/1380_IL10R_P176_IGO_10084_4_Aligned.out.sorted.tagged.sorted.bam.bai"

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

    return items
