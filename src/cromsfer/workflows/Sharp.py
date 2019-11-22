#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #     'Sharp.combinedClass': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HashedCountMatrix/final-classification.tsv.gz',
    #     'Sharp.combinedCountMatrix': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HashedCountMatrix/final-matrix.tsv.gz',
    #     'Sharp.combinedLog': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HashedCountMatrix/combine.log',
    #     'Sharp.combinedStats': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HashedCountMatrix/stats.yml',
    #     'Sharp.countReport': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-CiteSeqCount/results/run_report.yaml',
    #     'Sharp.fastQCR1Html': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-FastQCR1/IL10neg_HTO_IGO_10034_23_S2_R1_fastqc.html',
    #     'Sharp.fastQCR2Html': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-FastQCR2/IL10neg_HTO_IGO_10034_23_S2_R2_fastqc.html',
    #     'Sharp.htoClassification': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HtoDemuxKMeans/final-classification.tsv.gz',
    #     'Sharp.htoClassification_Suppl1': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HtoDemuxSeurat/outputs/classification.csv',
    #     'Sharp.htoClassification_Suppl2': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HtoDemuxSeurat/outputs/full-output.csv',
    #     'Sharp.htoClassification_Suppl3': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-CorrectFalsePositiveDoublets/final-classification.tsv.gz',
    #     'Sharp.logHtoDemux': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HtoDemuxKMeans/demux_kmeans.log',
    #     'Sharp.logHtoDemux_Suppl1': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-CorrectFalsePositiveDoublets/correct_fp_doublets.log',
    #     'Sharp.statsHtoDemux': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-HtoDemuxKMeans/stats.yml',
    #     'Sharp.statsHtoDemux_Suppl1': 'gs://chunj-cromwell/cromwell-execution/Sharp/8dad3d5a-59cd-4a45-8b41-43dd16817f2d/call-CorrectFalsePositiveDoublets/stats.yml'
    # }

    items = list()

    for key in outputs.keys():

        src = outputs[key]
        match = re.search(workflow_id + "/call-(.*)$", src)
        if match:
            items.append(
                (src, base_destination + "/" + match.group(1))
            )

    return items


def get_glob_list(workflow_id):

    items = [
        "HashedCountMatrix/*",
        "tag-list.csv"
    ]

    return items
