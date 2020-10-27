#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # "CiteSeq.umiCountMatrix": [
    #   "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/barcodes.tsv.gz",
    #   "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/features.tsv.gz",
    #   "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-CiteSeqCount/glob-5b2373ebac80816456a7726e786fc4d4/matrix.mtx.gz"
    # ],
    # "CiteSeq.fastQCR1Html": "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-FastQCR1/2091_CS1429a_T_1_CD45pos_citeseq_2_CITE_R1_fastqc.html",
    # "CiteSeq.readCountMatrix": [
    #   "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/barcodes.tsv.gz",
    #   "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/features.tsv.gz",
    #   "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-CiteSeqCount/glob-8e7f6a2dd9fb1323e5ebc5c1c063f6df/matrix.mtx.gz"
    # ],
    # "CiteSeq.adata": "s3://dp-lab-batch/cromwell-execution/CiteSeq/9c72e274-712a-4137-811c-4f1d6cc2eeb1/call-CiteSeqToAnnData/2091_CS1429a_T_1_CD45pos_citeseq_2_CITE.CITE-seq.h5ad",
    # "CiteSeq.countReport": "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-CiteSeqCount/results/run_report.yaml",
    # "CiteSeq.fastQCR2Html": "s3://dp-lab-batch/cromwell-execution/CiteSeq/eb5f81d3-cb16-4436-80f0-c8c0a2ed04d6/call-Preprocess/Preprocess/e96102a6-b8fc-4b51-990a-14ec9f61e854/call-FastQCR2/2091_CS1429a_T_1_CD45pos_citeseq_2_CITE_R2_fastqc.html"

    items = list()

    for key in outputs.keys():

        # skip if the value is null (e.g. File? out)
        if not outputs[key]:
            continue

        # is it a list of files from glob? (e.g. umiCountMatrix or readCountMatrix)
        if isinstance(outputs[key], list):
            # CiteSeq.umiCountMatrix --> umiCountMatrix
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
