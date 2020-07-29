#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    #     "mkref.outGtf": "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-FilterBiotypes/annotations.gtf",
    #     "mkref.outSTAR": [
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/Genome",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/SA",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/SAindex",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/chrLength.txt",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/chrName.txt",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/chrNameLength.txt",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/chrStart.txt",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/exonGeTrInfo.tab",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/exonInfo.tab",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/geneInfo.tab",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/genomeParameters.txt",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/sjdbInfo.txt",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/sjdbList.fromGTF.out.tab",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/sjdbList.out.tab",
    #       "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-RunSTAR/glob-aeb3bc502fb08c942c43aaeca3177a2a/transcriptInfo.tab"
    #     ],
    #     "mkref.outFilterLog": "s3://dp-lab-batch/cromwell-execution/mkref/7fc70703-9f7e-4b00-b93a-a2f271d5b7fb/call-FilterBiotypes/filter_biotypes.log"

    items = list()

    # we will flatten the hirarchical structure
    # copy everything to /outs
    for key in outputs.keys():

        # is it a list of files from glob? (e.g. fastqFiles)
        if isinstance(outputs[key], list):
            for file in outputs[key]:
                items.append((file, base_destination))
        else:
            # it's a single file
            file = outputs[key]
            items.append((file, base_destination))

    return items
