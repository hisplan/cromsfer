#!/usr/bin/env python
import re


def construct_src_dst_info(workflow_id, outputs, base_destination):

    # {
    #   "TransgenesCellRanger.outReferencePackage": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesCellRanger/33a69bd3-1fdc-44c0-9d7e-aece05f47390/call-mkref/AdultNepScrnaseq-CFP-TdTom.tar.gz",
    #   "TransgenesCellRanger.outFastaGzi": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesCellRanger/33a69bd3-1fdc-44c0-9d7e-aece05f47390/call-Transgenes/Transgenes/44fd84f4-981f-4096-97ce-ec426ad460c4/call-IndexCompressedFasta/cacheCopy/customGenome.fa.gz.gzi",
    #   "TransgenesCellRanger.outFilterLog": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesCellRanger/33a69bd3-1fdc-44c0-9d7e-aece05f47390/call-Transgenes/Transgenes/44fd84f4-981f-4096-97ce-ec426ad460c4/call-FilterBiotypes/cacheCopy/filter_biotypes.log",
    #   "TransgenesCellRanger.outFastaBgzip": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesCellRanger/33a69bd3-1fdc-44c0-9d7e-aece05f47390/call-Transgenes/Transgenes/44fd84f4-981f-4096-97ce-ec426ad460c4/call-ConcatenateFastas/cacheCopy/customGenome.fa.gz",
    #   "TransgenesCellRanger.outFastaFai": "s3://dp-lab-gwf-core/cromwell-execution/TransgenesCellRanger/33a69bd3-1fdc-44c0-9d7e-aece05f47390/call-Transgenes/Transgenes/44fd84f4-981f-4096-97ce-ec426ad460c4/call-IndexCompressedFasta/cacheCopy/customGenome.fa.gz.fai",
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
