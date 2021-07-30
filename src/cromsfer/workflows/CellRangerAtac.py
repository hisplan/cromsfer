#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "CellRangerATAC.summaryJson": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/summary.json",
    #   "CellRangerATAC.rawPeakBCMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/raw_peak_bc_matrix.h5",
    #   "CellRangerATAC.summaryHtml": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/web_summary.html",
    #   "CellRangerATAC.rawPeakBCMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-caf348d41af05d78d3c0df3d41bc4ba5/barcodes.tsv",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-caf348d41af05d78d3c0df3d41bc4ba5/matrix.mtx",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-caf348d41af05d78d3c0df3d41bc4ba5/peaks.bed"
    #   ],
    #   "CellRangerATAC.peakMotifMapping": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/peak_motif_mapping.bed",
    #   "CellRangerATAC.filteredTFBCMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/filtered_tf_bc_matrix.h5",
    #   "CellRangerATAC.pipestanceMeta": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/atac_pbmc_500_v1.mri.tgz",
    #   "CellRangerATAC.filteredPeakBCMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-dc314ee09c81a0f1ccb29faedd1adc0e/barcodes.tsv",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-dc314ee09c81a0f1ccb29faedd1adc0e/matrix.mtx",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-dc314ee09c81a0f1ccb29faedd1adc0e/peaks.bed"
    #   ],
    #   "CellRangerATAC.peakAnnotation": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/peak_annotation.tsv",
    #   "CellRangerATAC.cloupe": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/cloupe.cloupe",
    #   "CellRangerATAC.filteredTFBCMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-b263e0200860a34e22231270987a72da/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-b263e0200860a34e22231270987a72da/matrix.mtx.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/glob-b263e0200860a34e22231270987a72da/motifs.tsv"
    #   ],
    #   "CellRangerATAC.bam": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/possorted_bam.bam",
    #   "CellRangerATAC.secondaryAnalysis": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/analysis.tgz",
    #   "CellRangerATAC.summaryCsv": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/summary.csv",
    #   "CellRangerATAC.filteredPeakBCMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/filtered_peak_bc_matrix.h5",
    #   "CellRangerATAC.bai": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/possorted_bam.bam.bai",
    #   "CellRangerATAC.perBarcodeMetrics": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/singlecell.csv",
    #   "CellRangerATAC.peaks": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/peaks.bed",
    #   "CellRangerATAC.fragmentsIndex": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/fragments.tsv.gz.tbi",
    #   "CellRangerATAC.fragments": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerATAC/a8c959c6-1b6c-4083-9d0e-636d5f965424/call-Count/atac_pbmc_500_v1/outs/fragments.tsv.gz"
    # }

    items = list()

    for key in outputs.keys():

        # is it a list of files from glob? (e.g. CellRangerATAC.rawPeakBCMatrix)
        if isinstance(outputs[key], list):
            if key == "CellRangerATAC.rawPeakBCMatrix":
                subkey = "raw_peak_bc_matrix"
            elif key == "CellRangerATAC.filteredPeakBCMatrix":
                subkey = "filtered_peak_bc_matrix"
            elif key == "CellRangerATAC.filteredTFBCMatrix":
                subkey = "filtered_tf_bc_matrix"
            else:
                raise Exception("Unknown key: " + key)
            for file in outputs[key]:
                items.append((file, f"{base_destination}/{subkey}/"))
        else:
            # it's a single file
            file = outputs[key]
            items.append((file, base_destination + "/"))

    return items
