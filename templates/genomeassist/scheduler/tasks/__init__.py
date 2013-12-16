"""GenomeAssist Celery tasks."""
# These imports are necessary for Celery autodiscovery.
from .aligners import aligners
from .job import aggregate
