"""Tasks related to jobs as groups of aligner tasks."""


from __future__ import division
from collections import defaultdict
import json

import celery

from .aligners import aligners
from ..models import Job


@celery.task()
def aggregate(results):
    aggregated_result = defaultdict(float)
    for result in results:
        for alignment in result.alignments:
            aggregated_result[alignment.locus] += \
                alignment.quality / len(results)
    return dict(aggregated_result)


def start(job_id):
    # TODO:  Perform validation.
    job = Job.objects.get(pk=job_id)
    options = json.loads(job.options)
    subtasks = []
    for task_options in options:
        task = job.task_set.create(
            aligner=task_options['aligner'],
            name=task_options['name'],
            options=task_options['options'])
        task.save()
        subtasks.append(
            celery.current_app.tasks[aligners[task.aligner].name].s(task.id))
    subtask_group = celery.group(subtasks)
    result = celery.chord(subtask_group)(aggregate.s())
    job.celery_task_id = result.id
    job.save()
    return result
