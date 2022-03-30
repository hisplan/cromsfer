#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    # "ArchRCR.outFilteredPeakBCMtxHdf5": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/filtered_peak_bc_matrix.h5",
    # "ArchRCR.outAdata": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-ConstructAnnData/outs2/preprocessed.h5ad",
    # "ArchRCR.outBam": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/possorted_bam.bam",
    # "ArchRCR.outRawPeakBCMtxHdf5": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/raw_peak_bc_matrix.h5",
    # "ArchRCR.outPeaks": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/peaks.bed",
    # "ArchRCR.outLoupe": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/cloupe.cloupe",
    # "ArchRCR.outQC": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-744809ac5c14d4344041b890a4afd328/atac_pbmc_500_v1-Fragment_Size_Distribution.pdf",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-744809ac5c14d4344041b890a4afd328/atac_pbmc_500_v1-Pre-Filter-Metadata.rds",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-744809ac5c14d4344041b890a4afd328/atac_pbmc_500_v1-TSS_by_Unique_Frags.pdf"
    # ],
    # "ArchRCR.outPerBarcodeMetrics": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/singlecell.csv",
    # "ArchRCR.outFragments": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/fragments.tsv.gz",
    # "ArchRCR.outFilteredTFBCMtxHdf5": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/filtered_tf_bc_matrix.h5",
    # "ArchRCR.outBai": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/possorted_bam.bam.bai",
    # "ArchRCR.outFilteredTFBCMtx": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-b263e0200860a34e22231270987a72da/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-b263e0200860a34e22231270987a72da/matrix.mtx.gz",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-b263e0200860a34e22231270987a72da/motifs.tsv"
    # ],
    # "ArchRCR.outPeakAnnotation": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/peak_annotation.tsv",
    # "ArchRCR.outSummaryCsv": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/summary.csv",
    # "ArchRCR.outArrow0": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-5205b798d14ff0d1b415b8f1d26023b5/atac_pbmc_500_v1.arrow"
    # ],
    # "ArchRCR.outSummaryJson": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/summary.json",
    # "ArchRCR.outFileList": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/filelist-all.txt",
    # "ArchRCR.outRawPeakBCMtx": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-caf348d41af05d78d3c0df3d41bc4ba5/barcodes.tsv",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-caf348d41af05d78d3c0df3d41bc4ba5/matrix.mtx",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-caf348d41af05d78d3c0df3d41bc4ba5/peaks.bed"
    # ],
    # "ArchRCR.outPeakMotifMapping": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/peak_motif_mapping.bed",
    # "ArchRCR.outProject": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/outs.tgz",
    # "ArchRCR.outAnalysis": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/analysis.tgz",
    # "ArchRCR.outFragmentsIndex": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/fragments.tsv.gz.tbi",
    # "ArchRCR.outLogs": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addClusters-7771da8481-Date-2022-03-28_Time-15-45-22.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addGeneScoreMatrix-771d144b35-Date-2022-03-28_Time-15-45-26.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addGroupCoverages-7723f35ed3-Date-2022-03-28_Time-15-46-58.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addIterativeLSI-77525e565e-Date-2022-03-28_Time-15-44-31.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addPeakMatrix-7744a5ff12-Date-2022-03-28_Time-15-58-47.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-addReproduciblePeakSet-771baa1aa2-Date-2022-03-28_Time-15-54-18.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-createArrows-7731034910-Date-2022-03-28_Time-15-39-24.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-getMatrixFromProject-771f038c4f-Date-2022-03-28_Time-15-59-23.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-getMatrixFromProject-7754bc9760-Date-2022-03-28_Time-15-46-46.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-plotEmbedding-772b779fee-Date-2022-03-28_Time-15-46-39.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-plotEmbedding-7745e388c3-Date-2022-03-28_Time-15-46-39.log",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Run/glob-8aaae32edf6264c92ed2db3f0a4bc92e/ArchR-plotEmbedding-77641501e7-Date-2022-03-28_Time-15-46-39.log"
    # ],
    # "ArchRCR.outPipestanceMeta": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/pipestanceMeta.tgz",
    # "ArchRCR.outFilteredPeakBCMtx": [
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-dc314ee09c81a0f1ccb29faedd1adc0e/barcodes.tsv",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-dc314ee09c81a0f1ccb29faedd1adc0e/matrix.mtx",
    #     "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/glob-dc314ee09c81a0f1ccb29faedd1adc0e/peaks.bed"
    # ],
    # "ArchRCR.outSummaryHtml": "s3://dp-lab-gwf-core2/cromwell-execution/ArchRCR/dbb3c5b5-fbe4-4d2e-8bab-fe27299e2e2f/call-Count/atac_pbmc_500_v1/outs/web_summary.html"
    # }

    items = list()

    for key in outputs.keys():

        # is it a list of files from glob?
        if isinstance(outputs[key], list):
            if key == "ArchRCR.outArrow0":
                subkey = "arrows"
            elif key == "ArchRCR.outQC":
                subkey = "qc"
            elif key == "ArchRCR.outLogs":
                subkey = "logs"
            elif key == "ArchRCR.outRawPeakBCMtx":
                subkey = "raw_peak_bc_matrix"
            elif key == "ArchRCR.outFilteredPeakBCMtx":
                subkey = "filtered_peak_bc_matrix"
            elif key == "ArchRCR.outFilteredTFBCMtx":
                subkey = "filtered_tf_bc_matrix"
            else:
                raise Exception("Unknown key: " + key)
            for file in outputs[key]:
                items.append((file, f"{base_destination}/{subkey}/"))
        else:
            # it's a single file
            file = outputs[key]
            if key == "ArchRCR.outProject":
                items.append((file, base_destination + "/project.tgz"))
            else:
                items.append((file, base_destination + "/"))

    return items
