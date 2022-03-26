#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "MitoTracing.bam": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Align/Ru581b_T1_MITO_resequenced/outs/possorted_genome_bam.bam",
    #   "MitoTracing.bai": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Align/Ru581b_T1_MITO_resequenced/outs/possorted_genome_bam.bam.bai",
    #   "MitoTracing.filteredBam": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-RemoveSupplReads/Ru581b_T1_MITO_resequenced.mt.dedupe.splitn.bqsr.bam.filtered.sorted.bam"
    #   "MitoTracing.filteredBai": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-RemoveSupplReads/Ru581b_T1_MITO_resequenced.mt.dedupe.splitn.bqsr.bam.filtered.sorted.bam.bai",
    #   "MitoTracing.perBarcodeBamTar": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-PerBarcodeBam/glob-108b094e1f72432e5d4c19cba70ca98b/per-barcode.A.bam.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-PerBarcodeBam/glob-108b094e1f72432e5d4c19cba70ca98b/per-barcode.C.bam.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-PerBarcodeBam/glob-108b094e1f72432e5d4c19cba70ca98b/per-barcode.G.bam.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-PerBarcodeBam/glob-108b094e1f72432e5d4c19cba70ca98b/per-barcode.T.bam.tar"
    #   ],
    #   "MitoTracing.perBarcodeVcfTar": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Mutect2PerBarcode/shard-0/per-barcode.A.vcf.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Mutect2PerBarcode/shard-1/per-barcode.C.vcf.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Mutect2PerBarcode/shard-2/per-barcode.G.vcf.tar",
    #     "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Mutect2PerBarcode/shard-3/per-barcode.T.vcf.tar"
    #   ],
    #   "MitoTracing.vcf": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Mutect2/Ru581b_T1_MITO_resequenced.vcf.gz",
    #   "MitoTracing.vcfIdx": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Mutect2/Ru581b_T1_MITO_resequenced.vcf.gz.tbi",
    #   "MitoTracing.vcfStats": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Mutect2/Ru581b_T1_MITO_resequenced.vcf.gz.stats",
    #   "MitoTracing.referencePackage": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-MakeMitoRefPkg/mito-ref-pkg.tar.gz",
    #   "MitoTracing.metricsSummary": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Align/Ru581b_T1_MITO_resequenced/outs/metrics_summary.csv",
    #   "MitoTracing.perMoleculeInfo": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Align/Ru581b_T1_MITO_resequenced/outs/molecule_info.h5",
    #   "MitoTracing.pipestanceMeta": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Align/Ru581b_T1_MITO_resequenced/Ru581b_T1_MITO_resequenced.mri.tgz",
    #   "MitoTracing.webSummary": "s3://dp-lab-gwf-core/cromwell-execution/MitoTracing/3a73a18e-8527-4f0b-8256-87aaf3669433/call-Align/Ru581b_T1_MITO_resequenced/outs/web_summary.html",
    # }

    items = list()

    # we will flatten the hirarchical structure
    for key in outputs.keys():

        # is it a list of files from glob? (e.g. perBarcodeBamTar)
        if isinstance(outputs[key], list):
            for file in outputs[key]:
                items.append((file, base_destination + "/"))
        else:
            # it's a single file
            file = outputs[key]
            items.append((file, base_destination + "/"))

    return items
