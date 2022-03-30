#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "CiteSeq.umiCountMatrix": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/features.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/matrix.mtx.gz"
    #   ],
    #   "CiteSeq.fastQCR1Html": "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-FastQCR1/2090_CS1429a_T_1_CD45pos_citeseq_1_CITE_R1_fastqc.html",
    #   "CiteSeq.notebookQC": "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-BasicQC/2090_CS1429a_T_1_CD45pos_citeseq_1_CITE.QC.ipynb",
    #   "CiteSeq.htmlQC": "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-BasicQC/2090_CS1429a_T_1_CD45pos_citeseq_1_CITE.QC.html",
    #   "CiteSeq.readCountMatrix": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/features.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/matrix.mtx.gz"
    #   ],
    #   "CiteSeq.adata": "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-ToAnnData/2090_CS1429a_T_1_CD45pos_citeseq_1_CITE.h5ad",
    #   "CiteSeq.countReport": "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-CiteSeqCount/results/run_report.yaml",
    #   "CiteSeq.adataQC": "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-BasicQC/outputs/2090_CS1429a_T_1_CD45pos_citeseq_1_CITE.QC.h5ad",
    #   "CiteSeq.fastQCR2Html": "s3://dp-lab-gwf-core2/cromwell-execution/CiteSeq/f7109b96-9ecc-4a84-8ab1-6728d51d9831/call-Preprocess/Preprocess/a6d02153-e550-45fe-9a17-87c2968996c7/call-FastQCR2/2090_CS1429a_T_1_CD45pos_citeseq_1_CITE_R2_fastqc.html"
    # }

    items = list()

    items.append((outputs["CiteSeq.countReport"], base_destination + "/counts/"))

    for file in outputs["CiteSeq.umiCountMatrix"]:
        items.append((file, base_destination + "/counts/umis/"))

    for file in outputs["CiteSeq.readCountMatrix"]:
        items.append((file, base_destination + "/counts/reads/"))

    items.append((outputs["CiteSeq.adata"], base_destination + "/"))

    # QC related
    items.append((outputs["CiteSeq.fastQCR1Html"], base_destination + "/QC/fastqc/"))
    items.append((outputs["CiteSeq.fastQCR2Html"], base_destination + "/QC/fastqc/"))

    # only if found (backward compatibility)
    if "CiteSeq.htmlQC" in outputs:
        items.append((outputs["CiteSeq.htmlQC"], base_destination + "/QC/"))

    if "CiteSeq.notebookQC" in outputs:
        items.append((outputs["CiteSeq.notebookQC"], base_destination + "/QC/"))

    if "CiteSeq.adataQC" in outputs:
        items.append((outputs["CiteSeq.adataQC"], base_destination + "/QC/"))

    return items
