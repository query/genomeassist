"""Generic aligner tasks and functions."""


from collections import namedtuple
import inspect
import json
import os
import platform
import re
import resource
import subprocess
import tempfile
import urlparse

import celery
import celery.states

from ..models import Task


LINE_RE = re.compile(r'.+')


Alignment = namedtuple('Alignment', ['read', 'locus', 'quality', 'cigar'])
"""A container for information about a successful alignment."""


def sam_alignments(sam_output):
    """Parse the SAM output in *sam_output* and return a list of
    Alignment objects containing the read name, locus, quality, and
    CIGAR information for each successful alignment found."""
    alignments = []
    for match in LINE_RE.finditer(sam_output):
        line = match.group(0)
        # Ignore header lines.
        if line.startswith('@'):
            continue
        fields = line.split('\t')
        flags = int(fields[1])
        # If the query sequence for this read is unmapped, skip it.
        if flags & 0x04:
            continue
        alignments.append(Alignment(read=fields[0], locus=int(fields[3]),
                                    quality=int(fields[4]), cigar=fields[5]))
    return alignments


class AlignerResult(namedtuple('AlignerResult',
                               ['alignments', 'out', 'err', 'rusage'])):
    def __new__(cls, alignments, out, err, rusage):
        # rusage needs to be transformed into a dict, if it isn't one
        # already, before we can change any of its contents.
        if isinstance(rusage, resource.struct_rusage):
            rusage = dict((k, v) for k, v in inspect.getmembers(rusage)
                                 if k.startswith('ru_'))
        # ru_maxrss needs to be normalized based on the platform.
        # Linux uses kilobytes, Mac OS X uses bytes, and so forth.
        # We use bytes, so Linux results get multiplied by 1024.
        if 'ru_maxrss_normalized' not in rusage:
            rusage['ru_maxrss_normalized'] = rusage['ru_maxrss']
            if platform.system() == 'Linux':
                rusage['ru_maxrss_normalized'] *= 1024
        return super(AlignerResult, cls).__new__(
            cls, alignments, out, err, rusage)


class AlignerTask(celery.Task):
    """A Celery task for invoking a sequence aligner."""
    abstract = True  # This is not inherited by subclasses, thankfully.

    def parse_options(self, read, reference, options):
        """Return the appropriate command-line arguments for invoking
        this aligner on the given *read* and *reference* combination
        with the given *options*."""
        raise NotImplementedError

    def parse_output(self, out, err):
        """Return a list of Alignment objects based on results from the
        aligner's *out* and *err*."""
        raise NotImplementedError

    def run(self, task_id):
        task = Task.objects.get(pk=task_id)
        task.celery_task_id = self.request.id
        task.save()
        options = dict(urlparse.parse_qsl(task.options))
        args = self.parse_options(task.job.read.path,
                                  task.job.reference,
                                  options)
        outfile = tempfile.TemporaryFile()
        errfile = tempfile.TemporaryFile()
        child = subprocess.Popen(args, stdout=outfile, stderr=errfile)
        pid, returncode, rusage = os.wait4(child.pid, 0)
        outfile.seek(0)
        errfile.seek(0)
        out = outfile.read()
        err = errfile.read()
        outfile.close()
        errfile.close()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode=returncode,
                                                cmd=args, output=(out + err))
        return AlignerResult(alignments=self.parse_output(out, err),
                             out=out, err=err, rusage=rusage)
