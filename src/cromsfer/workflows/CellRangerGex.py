#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # "CellRangerGex.cloupe": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/cloupe.cloupe",
    # "CellRangerGex.rawFeatureBarcodeMatrix": [
    #   "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/glob-4429db8b5ffc30034fc8a4004f21bd93/barcodes.tsv.gz",
    #   "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/glob-4429db8b5ffc30034fc8a4004f21bd93/features.tsv.gz",
    #   "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/glob-4429db8b5ffc30034fc8a4004f21bd93/matrix.mtx.gz"
    # ],
    # "CellRangerGex.perMoleculeInfo": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/molecule_info.h5",
    # "CellRangerGex.metricsSummary": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/metrics_summary.csv",
    # "CellRangerGex.pipestance": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/Foxp3_minus.mri.tgz",
    # "CellRangerGex.bam": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/possorted_genome_bam.bam",
    # "CellRangerGex.filteredFeatureBarcodeMatrix": [
    #   "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/glob-62935234b8aecf770cbcee6a36b0ac4b/barcodes.tsv.gz",
    #   "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/glob-62935234b8aecf770cbcee6a36b0ac4b/features.tsv.gz",
    #   "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/glob-62935234b8aecf770cbcee6a36b0ac4b/matrix.mtx.gz"
    # ],
    # "CellRangerGex.outAnalysis": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/analysis.tgz",
    # "CellRangerGex.webSummary": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/web_summary.html",
    # "CellRangerGex.bai": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/possorted_genome_bam.bam.bai",
    # "CellRangerGex.debugFile": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/debug.tgz",
    # "CellRangerGex.filteredFeatureBarcodeMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/filtered_feature_bc_matrix.h5",
    # "CellRangerGex.rawFeatureBarcodeMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerGex/09e6f6a7-949b-48fd-8cfb-550000784346/call-Count/Foxp3_minus/outs/raw_feature_bc_matrix.h5"

    items = list()

    # copy everything to /outs
    for key in outputs.keys():

        # is it a list of files from glob? (e.g. CellRangerGex.filteredFeatureBarcodeMatrix)
        if isinstance(outputs[key], list):
            if key == "CellRangerGex.filteredFeatureBarcodeMatrix":
                subkey = "filtered_feature_bc_matrix"
            elif key == "CellRangerGex.rawFeatureBarcodeMatrix":
                subkey = "raw_feature_bc_matrix"
            else:
                raise Exception("Unknown key: " + key)
            for file in outputs[key]:
                items.append((file, f"{base_destination}/outs/{subkey}/"))
        else:
            # it's a single file
            file = outputs[key]
            items.append((file, base_destination + "/outs/"))

    return items
