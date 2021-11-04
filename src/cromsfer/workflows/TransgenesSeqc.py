#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "TransgenesSeqc.outStarFiles": [
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/Genome",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/SA",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/SAindex",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/annotations.gtf",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrLength.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrName.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrNameLength.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/chrStart.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/exonGeTrInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/exonInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/geneInfo.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/genomeParameters.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbInfo.txt",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbList.fromGTF.out.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/sjdbList.out.tab",
    #     "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-GenerateIndex/glob-20ebd8c9cf25515da3e6ce1213dba1ad/transcriptInfo.tab"
    #   ],
    #   "TransgenesSeqc.outFilterLog": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-Transgenes/Transgenes/c26e9c1a-3a76-45d9-988f-6889f4b382a8/call-FilterBiotypes/cacheCopy/filter_biotypes.log",
    #   "TransgenesSeqc.outFastaFai": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-Transgenes/Transgenes/c26e9c1a-3a76-45d9-988f-6889f4b382a8/call-IndexCompressedFasta/cacheCopy/customGenome.fa.gz.fai",
    #   "TransgenesSeqc.outFastaGzi": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-Transgenes/Transgenes/c26e9c1a-3a76-45d9-988f-6889f4b382a8/call-IndexCompressedFasta/cacheCopy/customGenome.fa.gz.gzi",
    #   "TransgenesSeqc.outFastaBgzip": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesSeqc/0e3efea6-7ca7-4229-af7f-0db7334bac9b/call-Transgenes/Transgenes/c26e9c1a-3a76-45d9-988f-6889f4b382a8/call-ConcatenateFastas/cacheCopy/customGenome.fa.gz"
    # }

    items = list()

    for key in outputs.keys():

        if key == "TransgenesSeqc.outStarFiles":
            for file in outputs[key]:
                items.append((file, base_destination + "/STAR-index/"))
        elif key.startswith("TransgenesSeqc.outFasta"):
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
