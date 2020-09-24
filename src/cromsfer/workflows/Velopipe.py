#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # "Velopipe.outPosSortedTaggedBai": "s3://dp-lab-batch/cromwell-execution/Velopipe/313c0570-7565-4eaf-823d-969e3fc5a8ae/call-PosSortedTaggedBam/1378_CMI_P176_IGO_10084_2_Aligned.out.sorted.tagged.sorted.bam.bai",
    # "Velopipe.outLoom": "s3://dp-lab-batch/cromwell-execution/Velopipe/313c0570-7565-4eaf-823d-969e3fc5a8ae/call-Velocyto/glob-6e284a9cd30ed4548d4059bf33133003/1378_CMI_P176_IGO_10084_2_Aligned_KHU2G.loom",
    # "Velopipe.outCBSortedTaggedBam": "s3://dp-lab-batch/cromwell-execution/Velopipe/313c0570-7565-4eaf-823d-969e3fc5a8ae/call-CBSortedTaggedBam/cellsorted_1378_CMI_P176_IGO_10084_2_Aligned.out.sorted.tagged.bam",
    # "Velopipe.outPosSortedTaggedBam": "s3://dp-lab-batch/cromwell-execution/Velopipe/313c0570-7565-4eaf-823d-969e3fc5a8ae/call-PosSortedTaggedBam/1378_CMI_P176_IGO_10084_2_Aligned.out.sorted.tagged.sorted.bam"

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
