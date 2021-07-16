#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "SeqcCustomGenes.outFasta": "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-ConcatenateFastas/customGenome.fa.gz",
    #   "SeqcCustomGenes.outFastaGzi": "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-IndexCompressedFasta/customGenome.fa.gz.gzi",
    #   "SeqcCustomGenes.outFastaFai": "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-IndexCompressedFasta/customGenome.fa.gz.fai",
    #   "SeqcCustomGenes.outSeqcFiles": null,
    #   "SeqcCustomGenes.outFilterLog": "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-FilterBiotypes/filter_biotypes.log",
    #   "SeqcCustomGenes.outStarFiles": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/Genome",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/SA",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/SAindex",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/annotations.gtf",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrLength.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrName.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrNameLength.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrStart.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/exonGeTrInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/exonInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/geneInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/genomeParameters.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbInfo.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbList.fromGTF.out.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbList.out.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/SeqcCustomGenes/b8916d74-7701-4e95-9c35-7b78e72beb98/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/transcriptInfo.tab"
    #   ]
    # }

    items = list()

    for key in outputs.keys():

        if key == "SeqcCustomGenes.outSeqcFiles":
            # fixme: not implemented
            pass
        elif key == "SeqcCustomGenes.outStarFiles":
            for file in outputs[key]:
                items.append(
                    (file, base_destination + "/STAR-index/")
                )
        elif key.startswith("SeqcCustomGenes.outFasta"):
            file = outputs[key]
            items.append(
                (file, base_destination + "/genome/")
            )
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
