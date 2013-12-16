import celery
from celery.result import AsyncResult
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from djcelery.models import TaskMeta

from .files import read_storage


class CeleryTaskWrapper(models.Model):
    """A model wrapping Celery TaskMeta data."""
    celery_task_id = models.CharField(max_length=255, null=True)

    class Meta(object):
        abstract = True

    def celery_task(self):
        """Return the TaskMeta model instance pointed to by this model
        instance, or None if there is no result yet."""
        return TaskMeta.objects.filter(task_id=self.celery_task_id).first()

    def __unicode__(self):
        if self.name:
            name = self.name
        else:
            name = u'Untitled'
        if self.celery_task_id:
            name += u' ({})'.format(self.celery_task_id)
        return name


class Job(CeleryTaskWrapper):
    """A collection of aligner tasks that operate on the same files,
    represented as a single unit in the frontend."""
    name = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    read = models.FileField(
        upload_to=(lambda job, fn: '{}.fq'.format(job.id)),
        storage=read_storage,
        verbose_name='Sequence data',
        help_text='A FASTQ sequence file containing the read to align '
                  'against the reference genome.')
    reference = models.FilePathField(
        verbose_name='Reference genome',
        allow_files=False,
        allow_folders=True,
        path=settings.SCHEDULER_REFERENCE_DIR)
    options = models.TextField(
        help_text='A JSON object containing a list of aligner tasks '
                  'and their associated options.')

    def save(self, *args, **kwargs):
        # Swap the read out temporarily on initial save, as the primary
        # key hasn't been set yet, and thus the read filename can't yet
        # be determined.
        if self.pk is None:
            read_ = self.read
            self.read = None
            super(Job, self).save(*args, **kwargs)
            self.read = read_
        # We now have a primary key, so it's safe to save the model
        # instance a second time, knowing that the read filename will
        # now be set properly.
        super(Job, self).save(*args, **kwargs)

    @property
    def state(self):
        """The current state of this job."""
        if self.celery_task_id:
            result = AsyncResult(id=self.celery_task_id)
            # We don't just invariably return result.state here, because
            # the Celery task pointed to by this job is the _callback_,
            # which is not started until after the child tasks have
            # finished.  Instead, we return result.state only if the
            # callback is ready (has been started), and otherwise loop
            # over the child tasks to determine whether or not they've
            # been started.
            if result.ready():
                return result.state
        for task in self.task_set.all():
            if (task.celery_task_id and
                    AsyncResult(id=task.celery_task_id).ready()):
                return celery.states.STARTED
        return celery.states.PENDING
admin.site.register(Job)


class Task(CeleryTaskWrapper):
    """Additional task-related information not provided by Celery."""
    job = models.ForeignKey(Job)
    aligner = models.CharField(max_length=15)
    name = models.CharField(max_length=255, blank=True)
    options = models.TextField(
        help_text="A JSON object containing this task's options.")

    @property
    def state(self):
        """The current state of this task."""
        if self.celery_task_id:
            return AsyncResult(id=self.celery_task_id).state
        return celery.states.PENDING
admin.site.register(Task)
