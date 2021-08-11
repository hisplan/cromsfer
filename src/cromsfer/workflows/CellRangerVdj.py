#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    #     "CellRangerVdj.bamFiles": [
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-80dbbf76f1093f70291ecebac4bc0971/all_contig.bam",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-80dbbf76f1093f70291ecebac4bc0971/all_contig.bam.bai",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-80dbbf76f1093f70291ecebac4bc0971/concat_ref.bam",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-80dbbf76f1093f70291ecebac4bc0971/concat_ref.bam.bai",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-80dbbf76f1093f70291ecebac4bc0971/consensus.bam",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-80dbbf76f1093f70291ecebac4bc0971/consensus.bam.bai"
    #     ],
    #     "CellRangerVdj.cellBarcodes": "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/Lmgp66_tet_replicate/outs/cell_barcodes.json",
    #     "CellRangerVdj.annotationFiles": [
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-02f73c8de85e32cc5d3abcebfa9335e4/all_contig_annotations.bed",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-02f73c8de85e32cc5d3abcebfa9335e4/all_contig_annotations.csv",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-02f73c8de85e32cc5d3abcebfa9335e4/all_contig_annotations.json",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-02f73c8de85e32cc5d3abcebfa9335e4/consensus_annotations.csv",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-02f73c8de85e32cc5d3abcebfa9335e4/consensus_annotations.json",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-02f73c8de85e32cc5d3abcebfa9335e4/filtered_contig_annotations.csv"
    #     ],
    #     "CellRangerVdj.pipestanceMeta": "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/Lmgp66_tet_replicate/Lmgp66_tet_replicate.mri.tgz",
    #     "CellRangerVdj.vloupe": "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/Lmgp66_tet_replicate/outs/vloupe.vloupe",
    #     "CellRangerVdj.fastaFiles": [
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-5ea969edb8af2b8b04e1b1ac96759bb3/all_contig.fasta",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-5ea969edb8af2b8b04e1b1ac96759bb3/all_contig.fasta.fai",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-5ea969edb8af2b8b04e1b1ac96759bb3/concat_ref.fasta",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-5ea969edb8af2b8b04e1b1ac96759bb3/concat_ref.fasta.fai",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-5ea969edb8af2b8b04e1b1ac96759bb3/consensus.fasta",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-5ea969edb8af2b8b04e1b1ac96759bb3/consensus.fasta.fai",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-5ea969edb8af2b8b04e1b1ac96759bb3/filtered_contig.fasta"
    #     ],
    #     "CellRangerVdj.metricsSummary": "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/Lmgp66_tet_replicate/outs/metrics_summary.csv",
    #     "CellRangerVdj.fastqFiles": [
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-6b883bfc0336906e72a285bf6612ed17/all_contig.fastq",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-6b883bfc0336906e72a285bf6612ed17/consensus.fastq",
    #       "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/glob-6b883bfc0336906e72a285bf6612ed17/filtered_contig.fastq"
    #     ],
    #     "CellRangerVdj.webSummary": "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/Lmgp66_tet_replicate/outs/web_summary.html",
    #     "CellRangerVdj.clonotypes": "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/Lmgp66_tet_replicate/outs/clonotypes.csv",
    #     "CellRangerVdj.debugFile": "s3://dp-lab-batch/cromwell-execution/CellRangerVdj/4b41842f-2ed0-49cb-a9b6-d8871b019fae/call-Vdj/debug.tgz"

    items = list()

    # we will flatten the hirarchical structure
    for key in outputs.keys():

        # is it a list of files from glob? (e.g. fastqFiles)
        if isinstance(outputs[key], list):
            for file in outputs[key]:
                items.append((file, base_destination + "/"))
        else:
            # it's a single file
            file = outputs[key]
            items.append((file, base_destination + "/"))

    return items
