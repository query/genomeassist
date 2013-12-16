"""Dummy aligners for testing."""


from time import sleep

from ..aligner import AlignerTask


class Success(AlignerTask):
    def parse_options(self, read, reference, options):
        sleep(float(options.get('sleep', 20)))
        return ['true']

    def parse_output(self, out, err):
        return []


class Failure(AlignerTask):
    def parse_options(self, read, reference, options):
        sleep(float(options.get('sleep', 20)))
        return ['nonexistent_program']
