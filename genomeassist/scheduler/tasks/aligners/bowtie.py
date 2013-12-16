"""Bowtie aligner frontend."""


import os.path

from django.conf import settings

from ..aligner import AlignerTask, sam_alignments


class Bowtie(AlignerTask):
    def parse_options(self, read, reference, options):
        args = [os.path.join(settings.SCHEDULER_BIN_DIR, 'bowtie')]
        args.append('-S')  # SAM output format.
        args.append('--sam-nohead')  # Bowtie's SAM headers reveal
                                     # information about server paths.
        if options.get('alignment') == 'v':
            args.append('-v')
            args.append(options.get('v', '0'))
        else:
            args.append('-n')
            args.append(options.get('seedmms', '2'))
            if 'seedlen' in options:
                args.append('-l')
                args.append(options['seedlen'])
            if 'maqerr' in options:
                args.append('-e')
                args.append(options['maqerr'])
            if 'nomaqround' in options:
                args.append('--nomaqround')
        if options.get('reporting') == 'a':
            args.append('-a')
        else:
            args.append('-k')
            args.append(options.get('k', '1'))
        if options.get('m'):
            args.append('-m')
            args.append(options['m'])
        if options.get('order') == 'best':
            args.append('--best')
            if 'strata' in options:
                args.append('--strata')
        args.append(os.path.join(reference, 'genome'))
        args.append(read)
        return args

    def parse_output(self, out, err):
        return sam_alignments(out)
