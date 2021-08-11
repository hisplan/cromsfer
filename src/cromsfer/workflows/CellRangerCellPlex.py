#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

# {
#   "CellRangerCellPlex.rawMoleculeInfoH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/count/raw_molecule_info.h5",
#   "CellRangerCellPlex.tagCallesPerCell": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/multiplexing_analysis/tag_calls_per_cell.csv",
#   "CellRangerCellPlex.multiConfig": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/multi.config.csv",
#   "CellRangerCellPlex.featureReference": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/count/feature_reference.csv",
#   "CellRangerCellPlex.tagCallsSummary": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/multiplexing_analysis/tag_calls_summary.csv",
#   "CellRangerCellPlex.rawFeatureBCMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/count/raw_feature_bc_matrix.h5",
#   "CellRangerCellPlex.rawFeatureBCMatrix": [
#     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/glob-04d033f2e7cde963f065ef4b5ac72127/barcodes.tsv.gz",
#     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/glob-04d033f2e7cde963f065ef4b5ac72127/features.tsv.gz",
#     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/glob-04d033f2e7cde963f065ef4b5ac72127/matrix.mtx.gz"
#   ],
#   "CellRangerCellPlex.unassignedBam": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/count/unassigned_alignments.bam",
#   "CellRangerCellPlex.perSampleOuts": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/per-sample-outs.tgz",
#   "CellRangerCellPlex.cloupe": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/count/raw_cloupe.cloupe",
#   "CellRangerCellPlex.unassignedBai": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/count/unassigned_alignments.bam.bai",
#   "CellRangerCellPlex.pipestanceMeta": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/109_pooled_cellplex.mri.tgz",
#   "CellRangerCellPlex.cellsPerTag": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/multiplexing_analysis/cells_per_tag.json",
#   "CellRangerCellPlex.assignmentConfidenceTable": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/464065b1-ae2a-4157-8361-e95355c9f0ce/call-Multi/109_pooled_cellplex/outs/multi/multiplexing_analysis/assignment_confidence_table.csv"
# }

    items = list()

    for key in outputs.keys():

        file = outputs[key]
        if isinstance(file, list):
            if key == "CellRangerCellPlex.rawFeatureBCMatrix":
                subkey = "raw_feature_bc_matrix"
            else:
                raise Exception("Unknown key: " + key)
            for f in file:
                items.append((f, f"{base_destination}/multi/count/{subkey}/"))
        else:
            if "/outs/multi/count/" in file:
                items.append((file, base_destination + "/multi/count/"))
            elif "/outs/multi/multiplexing_analysis" in file:
                items.append((file, base_destination + "/multi/multiplexing_analysis/"))
            else:
                items.append((file, base_destination + "/"))

    return items
