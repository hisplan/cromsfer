#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    #   "ArchRSA.outFileList": "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/filelist-all.txt",
    #   "ArchRSA.outArrow0": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-5205b798d14ff0d1b415b8f1d26023b5/DACE657_mKate2.arrow"
    #   ],
    #   "ArchRSA.outQC": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-744809ac5c14d4344041b890a4afd328/DACE657_mKate2-Fragment_Size_Distribution.pdf",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-744809ac5c14d4344041b890a4afd328/DACE657_mKate2-Pre-Filter-Metadata.rds",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-744809ac5c14d4344041b890a4afd328/DACE657_mKate2-TSS_by_Unique_Frags.pdf"
    #   ],
    #   "ArchRSA.outLogs": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addClusters-462a85d116-Date-2021-07-14_Time-01-19-14.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addGeneScoreMatrix-4657c1565-Date-2021-07-14_Time-01-19-28.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addGroupCoverages-464cbafe40-Date-2021-07-14_Time-01-24-07.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addIterativeLSI-464dd5317c-Date-2021-07-14_Time-01-16-19.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addPeakMatrix-461aff01b0-Date-2021-07-14_Time-02-03-04.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addReproduciblePeakSet-46c01ba73-Date-2021-07-14_Time-01-40-58.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-createArrows-46205c9681-Date-2021-07-14_Time-00-55-00.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-getMatrixFromProject-46407788c8-Date-2021-07-14_Time-01-22-17.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-getMatrixFromProject-46be0dfba-Date-2021-07-14_Time-02-04-21.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-plotEmbedding-4626ecfc97-Date-2021-07-14_Time-01-22-10.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-plotEmbedding-466355e99f-Date-2021-07-14_Time-01-22-10.log",
    #     "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-plotEmbedding-46a8a1395-Date-2021-07-14_Time-01-22-11.log"
    #   ],
    #   "ArchRSA.outProject": "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-Run/outs.tgz",
    #   "ArchRSA.outAdata": "s3://dp-lab-gwf-core/cromwell-execution/ArchRSA/fa2b7926-3524-4b40-8f84-e4d785f4a488/call-ConstructAnnData/outs2/preprocessed.h5ad"

    items = list()

    for key in outputs.keys():

        # is it a list of files from glob?
        if isinstance(outputs[key], list):
            if key == "ArchRSA.outArrow0":
                subkey = "arrows"
            elif key == "ArchRSA.outQC":
                subkey = "qc"
            elif key == "ArchRSA.outLogs":
                subkey = "logs"
            else:
                raise Exception("Unknown key: " + key)
            for file in outputs[key]:
                items.append((file, f"{base_destination}/{subkey}/"))
        else:
            # it's a single file
            file = outputs[key]
            if key == "ArchRSA.outProject":
                items.append((file, base_destination + "/project.tgz"))
            else:
                items.append((file, base_destination + "/"))

    return items
