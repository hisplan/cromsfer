#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #     'FastQC.FastQC.outHtml': [
    #         's3://dp-lab-batch/cromwell-execution/FastQC/f537c280-2b9c-43cd-ac70-43bf0767b0c4/call-FastQC/shard-0/472_B6_gp66_tet_d7_IGO_09290_1_S2_L001_I1_001_fastqc.html',
    #         's3://dp-lab-batch/cromwell-execution/FastQC/f537c280-2b9c-43cd-ac70-43bf0767b0c4/call-FastQC/shard-1/472_B6_gp66_tet_d7_IGO_09290_1_S2_L001_R1_001_fastqc.html',
    #         's3://dp-lab-batch/cromwell-execution/FastQC/f537c280-2b9c-43cd-ac70-43bf0767b0c4/call-FastQC/shard-2/472_B6_gp66_tet_d7_IGO_09290_1_S2_L001_R2_001_fastqc.html'
    #     ],
    #     'FastQC.FastQC.outZip': [
    #         's3://dp-lab-batch/cromwell-execution/FastQC/f537c280-2b9c-43cd-ac70-43bf0767b0c4/call-FastQC/shard-0/472_B6_gp66_tet_d7_IGO_09290_1_S2_L001_I1_001_fastqc.zip',
    #         's3://dp-lab-batch/cromwell-execution/FastQC/f537c280-2b9c-43cd-ac70-43bf0767b0c4/call-FastQC/shard-1/472_B6_gp66_tet_d7_IGO_09290_1_S2_L001_R1_001_fastqc.zip',
    #         's3://dp-lab-batch/cromwell-execution/FastQC/f537c280-2b9c-43cd-ac70-43bf0767b0c4/call-FastQC/shard-2/472_B6_gp66_tet_d7_IGO_09290_1_S2_L001_R2_001_fastqc.zip'
    #     ]
    # }

    items = list()

    for key in outputs.keys():

        for file in outputs[key]:
            items.append(
                (file, base_destination + "/")
            )

    return items
