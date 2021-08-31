#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # "CellRangerArc.gexBai": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/gex_possorted_bam.bam.bai",
    # "CellRangerArc.cloupe": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/cloupe.cloupe",
    # "CellRangerArc.peaks": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/atac_peaks.bed",
    # "CellRangerArc.webSummary": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/web_summary.html",
    # "CellRangerArc.pipestanceMeta": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/DACE657_mKate2.mri.tgz",
    # "CellRangerArc.atacBai": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/atac_possorted_bam.bam.bai",
    # "CellRangerArc.libraries": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/libraries.csv",
    # "CellRangerArc.peakAnnotation": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/atac_peak_annotation.tsv",
    # "CellRangerArc.filteredFeatureBCMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/filtered_feature_bc_matrix.h5",
    # "CellRangerArc.secondaryAnalysis": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/analysis.tgz",
    # "CellRangerArc.perBarcodeMetrics": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/per_barcode_metrics.csv",
    # "CellRangerArc.atacBam": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/atac_possorted_bam.bam",
    # "CellRangerArc.filteredFeatureBCMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/glob-f3b28021496efc355d46e520ed69b9d1/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/glob-f3b28021496efc355d46e520ed69b9d1/features.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/glob-f3b28021496efc355d46e520ed69b9d1/matrix.mtx.gz"
    # ],
    # "CellRangerArc.rawFeatureBCMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/raw_feature_bc_matrix.h5",
    # "CellRangerArc.rawFeatureBCMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/glob-16b07a2bb352afad0109608d41386e21/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/glob-16b07a2bb352afad0109608d41386e21/features.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/glob-16b07a2bb352afad0109608d41386e21/matrix.mtx.gz"
    # ],
    # "CellRangerArc.atacFragments": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/atac_fragments.tsv.gz",
    # "CellRangerArc.gexBam": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/gex_possorted_bam.bam",
    # "CellRangerArc.cutSites": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/atac_cut_sites.bigwig",
    # "CellRangerArc.atacFragmentsIndex": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/atac_fragments.tsv.gz.tbi",
    # "CellRangerArc.gexPerMoleculeInfo": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/gex_molecule_info.h5",
    # "CellRangerArc.metricsSummary": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerArc/09b8220a-6c24-4e69-b2e2-4e7856e5ddbd/call-Count/DACE657_mKate2/outs/summary.csv"

    items = list()

    for key in outputs.keys():

        # is it a list of files from glob? (e.g. CellRangerArc.filteredFeatureBCMatrix)
        if isinstance(outputs[key], list):
            if key == "CellRangerArc.filteredFeatureBCMatrix":
                subkey = "filtered_feature_bc_matrix"
            elif key == "CellRangerArc.rawFeatureBCMatrix":
                subkey = "raw_feature_bc_matrix"
            else:
                raise Exception("Unknown key: " + key)
            for file in outputs[key]:
                items.append((file, f"{base_destination}/{subkey}/"))
        else:
            # it's a single file
            file = outputs[key]
            items.append((file, base_destination + "/"))

    return items
