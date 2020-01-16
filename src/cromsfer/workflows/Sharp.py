#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    # "Sharp.fastQCR1Html": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-FastQCR1/1687_LX33_1_4_1_HTO_R1_fastqc.html",
    # "Sharp.countReport": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CiteSeqCount/results/run_report.yaml",
    # "Sharp.logHtoDemux": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HtoDemuxKMeans/demux_kmeans.log",
    # "Sharp.umiCountMatrix": [
    #     "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/barcodes.tsv.gz",
    #     "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/features.tsv.gz",
    #     "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/matrix.mtx.gz"
    # ],
    # "Sharp.readCountMatrix": [
    #     "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/barcodes.tsv.gz",
    #     "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/features.tsv.gz",
    #     "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/matrix.mtx.gz"
    # ],
    # "Sharp.logHtoDemux_Suppl1": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CorrectFalsePositiveDoublets/correct_fp_doublets.log",
    # "Sharp.combinedCountMatrix": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HashedCountMatrix/final-matrix.tsv.gz",
    # "Sharp.htoClassification_Suppl1": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HtoDemuxSeurat/outputs/classification.csv",
    # "Sharp.statsHtoDemux": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HtoDemuxKMeans/stats.yml",
    # "Sharp.statsHtoDemux_Suppl1": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CorrectFalsePositiveDoublets/stats.yml",
    # "Sharp.combinedLog": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HashedCountMatrix/combine.log",
    # "Sharp.fastQCR2Html": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-FastQCR2/1687_LX33_1_4_1_HTO_R2_fastqc.html",
    # "Sharp.combinedStats": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HashedCountMatrix/stats.yml",
    # "Sharp.htoClassification_Suppl2": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HtoDemuxSeurat/outputs/full-output.csv",
    # "Sharp.htoClassification": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HtoDemuxKMeans/final-classification.tsv.gz",
    # "Sharp.combinedClass": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-HashedCountMatrix/final-classification.tsv.gz",
    # "Sharp.htoClassification_Suppl3": "s3://dp-lab-batch/cromwell-execution/Sharp/b4a27cc5-9b8f-49f8-830e-1a65a477c8c1/call-CorrectFalsePositiveDoublets/final-classification.tsv.gz"
    # }

    items = list()

    for key in outputs.keys():

        # skip if the value is null (e.g. File? out)
        if not outputs[key]:
            continue

        # is it a list of files from glob? (e.g. umiCountMatrix or readCountMatrix)
        if isinstance(outputs[key], list):
            # Sharp.umiCountMatrix --> umiCountMatrix
            subfolder = key.split(".")[1]
            for src in outputs[key]:
                match = re.search(workflow_id + "/call-(.*?)/", src)
                if match:
                    items.append(
                        (src, base_destination + "/" + match.group(1) + "/" + subfolder + "/")
                    )
        else:
            # it's a single file
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
        "CiteSeqCount/*",
        "tag-list.csv"
    ]

    return items
