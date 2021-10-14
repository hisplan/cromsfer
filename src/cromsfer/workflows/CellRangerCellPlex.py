#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "CellRangerCellPlex.rawMoleculeInfoH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/count/raw_molecule_info.h5",
    #   "CellRangerCellPlex.tagCallesPerCell": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/multiplexing_analysis/tag_calls_per_cell.csv",
    #   "CellRangerCellPlex.multiConfig": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/multi.config.csv",
    #   "CellRangerCellPlex.featureReference": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/count/feature_reference.csv",
    #   "CellRangerCellPlex.tagCallsSummary": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/multiplexing_analysis/tag_calls_summary.csv",
    #   "CellRangerCellPlex.rawFeatureBCMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/count/raw_feature_bc_matrix.h5",
    #   "CellRangerCellPlex.rawFeatureBCMatrix": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-d1ce5784671bd9f62154c83e33c1c4f1/barcodes.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-d1ce5784671bd9f62154c83e33c1c4f1/features.tsv.gz",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-d1ce5784671bd9f62154c83e33c1c4f1/matrix.mtx.gz"
    #   ],
    #   "CellRangerCellPlex.unassignedBam": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/count/unassigned_alignments.bam",
    #   "CellRangerCellPlex.perSampleOuts": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-1d55e8282cca803a47fdef177a14a639/C5_1.outs.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-1d55e8282cca803a47fdef177a14a639/KPC_2.outs.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-1d55e8282cca803a47fdef177a14a639/KPF2_Lplus.outs.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-1d55e8282cca803a47fdef177a14a639/KPF3_Lplus.outs.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-1d55e8282cca803a47fdef177a14a639/PDEC_H9_PM_Ch.outs.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/glob-1d55e8282cca803a47fdef177a14a639/PDEC_H9_PT_Ch.outs.tar"
    #   ],
    #   "CellRangerCellPlex.cloupe": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/count/raw_cloupe.cloupe",
    #   "CellRangerCellPlex.unassignedBai": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/count/unassigned_alignments.bam.bai",
    #   "CellRangerCellPlex.pipestanceMeta": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/CellLines.mri.tgz",
    #   "CellRangerCellPlex.cellsPerTag": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/multiplexing_analysis/cells_per_tag.json",
    #   "CellRangerCellPlex.perSampleOutsSummary": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/per-sample-outs-summary.tar",
    #   "CellRangerCellPlex.assignmentConfidenceTable": "s3://dp-lab-gwf-core/cromwell-execution/CellRangerCellPlex/b2fa0551-ef77-4109-ac2b-64885b2ee450/call-Multi/CellLines/outs/multi/multiplexing_analysis/assignment_confidence_table.csv"
    # }

    items = list()

    for key in outputs.keys():

        file = outputs[key]
        if isinstance(file, list):
            if key == "CellRangerCellPlex.rawFeatureBCMatrix":
                for f in file:
                    items.append(
                        (f, f"{base_destination}/multi/count/raw_feature_bc_matrix/")
                    )
            elif key == "CellRangerCellPlex.perSampleOuts":
                for f in file:
                    items.append((f, f"{base_destination}/per_sample_outs/"))
            else:
                raise Exception("Unknown key: " + key)
        else:
            if "/outs/multi/count/" in file:
                items.append((file, base_destination + "/multi/count/"))
            elif "/outs/multi/multiplexing_analysis" in file:
                items.append((file, base_destination + "/multi/multiplexing_analysis/"))
            else:
                items.append((file, base_destination + "/"))

    return items
