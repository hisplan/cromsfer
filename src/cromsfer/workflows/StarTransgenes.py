#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "StarTransgenes.outFastaGzi": "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-IndexCompressedFasta/customGenome.fa.gz.gzi",
    #   "StarTransgenes.outFilterLog": "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-FilterBiotypes/filter_biotypes.log",
    #   "StarTransgenes.outFastaFai": "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-IndexCompressedFasta/customGenome.fa.gz.fai",
    #   "StarTransgenes.outFasta": "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-ConcatenateFastas/customGenome.fa.gz",
    #   "StarTransgenes.outStarFiles": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/Genome",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/SA",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/SAindex",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/annotations.gtf",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrLength.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrName.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrNameLength.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrStart.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/exonGeTrInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/exonInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/geneInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/genomeParameters.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbInfo.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbList.fromGTF.out.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbList.out.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/StarTransgenes/023777ca-0e35-437f-9b25-10c2e0f1f10a/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/transcriptInfo.tab"
    #   ]
    # }

    items = list()

    for key in outputs.keys():

        if key == "StarTransgenes.outStarFiles":
            for file in outputs[key]:
                items.append((file, base_destination + "/STAR-index/"))
        elif key.startswith("StarTransgenes.outFasta"):
            file = outputs[key]
            items.append((file, base_destination + "/genome/"))
        else:
            # is it a list of files from glob? (e.g. fastqFiles)
            if isinstance(outputs[key], list):
                for file in outputs[key]:
                    items.append((file, base_destination + "/"))
            else:
                # it's a single file
                file = outputs[key]
                items.append((file, base_destination + "/"))

    return items
