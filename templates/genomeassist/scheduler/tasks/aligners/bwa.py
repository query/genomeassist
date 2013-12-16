"""BWA aligner frontend."""


import os.path

from django.conf import settings

from ..aligner import AlignerTask, sam_alignments


class BWA(AlignerTask):
    def parse_options(self, read, reference, options):
        args = [os.path.join(settings.SCHEDULER_BIN_DIR, 'bwa'), 'mem']
        args.append(os.path.join(reference, 'genome.fa'))
        args.append(read)
        return args

    def parse_output(self, out, err):
        return sam_alignments(out)
