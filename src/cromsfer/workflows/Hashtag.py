#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    # "Hashtag.umiCountMatrix": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/features.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/matrix.mtx.gz"
    # ],
    # "Hashtag.countReport": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-CiteSeqCount/results/run_report.yaml",
    # "Hashtag.fastQCR1Html": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-FastQCR1/BF-1402_SI_R1_fastqc.html",
    # "Hashtag.fastQCR2Html": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-FastQCR2/BF-1402_SI_R2_fastqc.html",
    # "Hashtag.combinedCountMatrix": null,
    # "Hashtag.adataRaw": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-ToAnnData/BF-1402_SI.h5ad",
    # "Hashtag.adataFinal": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-UpdateAnnData/BF-1402_SI.h5ad",
    # "Hashtag.statsHtoDemux_Suppl1": null,
    # "Hashtag.adataQC": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-BasicQC/outputs/BF-1402_SI.QC.h5ad",
    # "Hashtag.combinedClass": null,
    # "Hashtag.htoClassification_Suppl1": null,
    # "Hashtag.logHtoDemux_Suppl1": null,
    # "Hashtag.htoClassification": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-HtoDemuxKMeans/classification.tsv.gz",
    # "Hashtag.combinedStats": null,
    # "Hashtag.htmlQC": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-BasicQC/BF-1402_SI.QC.html",
    # "Hashtag.statsHtoDemux": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-HtoDemuxKMeans/stats.yml",
    # "Hashtag.readCountMatrix": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/features.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-Preprocess/Preprocess/4f886adb-502d-4221-a9e1-9c6cb3d6c2a4/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/matrix.mtx.gz"
    # ],
    # "Hashtag.notebookQC": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-BasicQC/BF-1402_SI.QC.ipynb",
    # "Hashtag.htoClassification_Suppl3": null,
    # "Hashtag.combinedLog": null,
    # "Hashtag.htoClassification_Suppl2": null,
    # "Hashtag.logHtoDemux": "s3://dp-lab-gwf-core2/cromwell-execution/Hashtag/91708d0b-f46a-46c1-8f86-7337a9878164/call-HtoDemuxKMeans/demux_kmeans.log"
    # }

    items = list()

    items.append((outputs["Hashtag.countReport"], base_destination + "/counts/"))

    for file in outputs["Hashtag.umiCountMatrix"]:
        items.append((file, base_destination + "/counts/umis/"))

    for file in outputs["Hashtag.readCountMatrix"]:
        items.append((file, base_destination + "/counts/reads/"))

    items.append((outputs["Hashtag.adataRaw"], base_destination + "/"))
    items.append((outputs["Hashtag.adataFinal"], base_destination + "/"))

    # optional output
    if outputs["Hashtag.combinedCountMatrix"]:
        items.append((outputs["Hashtag.combinedCountMatrix"], base_destination + "/"))

    # optional output
    if outputs["Hashtag.combinedClass"]:
        items.append((outputs["Hashtag.combinedClass"], base_destination + "/"))

    # QC related
    items.append((outputs["Hashtag.fastQCR1Html"], base_destination + "/QC/fastqc/"))
    items.append((outputs["Hashtag.fastQCR2Html"], base_destination + "/QC/fastqc/"))

    # only if found (backward compatibility)
    if "Hashtag.htmlQC" in outputs:
        items.append((outputs["Hashtag.htmlQC"], base_destination + "/QC/"))

    if "Hashtag.notebookQC" in outputs:
        items.append((outputs["Hashtag.notebookQC"], base_destination + "/QC/"))

    if "Hashtag.adataQC" in outputs:
        items.append((outputs["Hashtag.adataQC"], base_destination + "/QC/"))

    return items
