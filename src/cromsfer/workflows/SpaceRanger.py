#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "SpaceRanger.rawFeatureBarcodeMatrix": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/raw_feature_bc_matrix.tgz",
    #   "SpaceRanger.loupe": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/cloupe.cloupe",
    #   "SpaceRanger.spatialEnrichment": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/spatial_enrichment.csv",
    #   "SpaceRanger.bam": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/possorted_genome_bam.bam",
    #   "SpaceRanger.analysis": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/analysis.tgz",
    #   "SpaceRanger.pipestanceMeta": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/MH-1300_V19T19-009_A1.mri.tgz",
    #   "SpaceRanger.metricsSummary": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/metrics_summary.csv",
    #   "SpaceRanger.perMoleculeInfo": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/molecule_info.h5",
    #   "SpaceRanger.filteredFeatureBarcodeMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/filtered_feature_bc_matrix.h5",
    #   "SpaceRanger.rawFeatureBarcodeMatrixH5": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/raw_feature_bc_matrix.h5",
    #   "SpaceRanger.spatial": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/spatial.tgz",
    #   "SpaceRanger.filteredFeatureBarcodeMatrix": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/filtered_feature_bc_matrix.tgz",
    #   "SpaceRanger.bai": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/possorted_genome_bam.bam.bai",
    #   "SpaceRanger.webSummary": "s3://dp-lab-gwf-core/cromwell-execution/SpaceRanger/2d9785eb-b15c-4f97-ad72-958cea74e762/call-Count/MH-1300_V19T19-009_A1/outs/web_summary.html"
    # }

    items = list()

    for key in outputs.keys():

        if isinstance(outputs[key], list):
            pass
        else:
            # it's a single file
            file = outputs[key]
            items.append((file, base_destination + "/"))

    return items
