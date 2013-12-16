"""Celery tasks for invoking individual aligners."""


# Dictionary of known aligners.

from .bowtie import Bowtie
from .bwa import BWA
from .dummy import Success, Failure

aligners = {
    'success': Success,
    'failure': Failure,

    'bowtie': Bowtie,
    'bwa': BWA,
}
