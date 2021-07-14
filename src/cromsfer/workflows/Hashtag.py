#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # "Sharp.fastQCR1Html": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-FastQCR1/1906_shK_052720_HTO_R1_fastqc.html",
    # "Sharp.countReport": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-CiteSeqCount/results/run_report.yaml",
    # "Sharp.logHtoDemux": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-HtoDemuxKMeans/demux_kmeans.log",
    # "Sharp.umiCountMatrix": [
    #   "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/barcodes.tsv.gz",
    #   "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/features.tsv.gz",
    #   "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/matrix.mtx.gz"
    # ],
    # "Sharp.readCountMatrix": [
    #   "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/barcodes.tsv.gz",
    #   "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/features.tsv.gz",
    #   "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/matrix.mtx.gz"
    # ],
    # "Sharp.logHtoDemux_Suppl1": null,
    # "Sharp.combinedCountMatrix": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-HashedCountMatrix/final-matrix.tsv.gz",
    # "Sharp.htoClassification_Suppl1": null,
    # "Sharp.statsHtoDemux": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-HtoDemuxKMeans/stats.yml",
    # "Sharp.statsHtoDemux_Suppl1": null,
    # "Sharp.combinedLog": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-HashedCountMatrix/combine.log",
    # "Sharp.fastQCR2Html": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-Preprocess/Preprocess/fc39fbeb-de43-41e0-b034-103e707ccb8d/call-FastQCR2/1906_shK_052720_HTO_R2_fastqc.html",
    # "Sharp.combinedStats": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-HashedCountMatrix/stats.yml",
    # "Sharp.htoClassification_Suppl2": null,
    # "Sharp.htoClassification": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-HtoDemuxKMeans/classification.tsv.gz",
    # "Sharp.combinedClass": "s3://dp-lab-batch/cromwell-execution/Sharp/fffc6852-28c2-4a0b-9698-27e5e85fd951/call-HashedCountMatrix/final-classification.tsv.gz",
    # "Sharp.htoClassification_Suppl3": null

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
            match = re.search(workflow_id + ".*/call-(.*)$", src)
            if match:
                items.append(
                    (src, base_destination + "/" + match.group(1))
                )

    return items


def get_glob_list(workflow_id):

    items = [
        "CiteSeqCount/*",
        "HashedCountMatrix/*",
        "Preprocess/*",
        "tag-list.csv"
    ]

    return items
