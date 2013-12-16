from __future__ import division
import os.path

from celery.result import AsyncResult
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.views.generic import ListView

from .forms import JobForm
from .models import Job
from .tasks.aligners import aligners
from .tasks.job import start as start_job


@login_required
def create(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.owner = request.user
            job.save()
            start_job(job.id)
            return HttpResponseRedirect(
                reverse('scheduler:detail', args=[job.id]))
    else:
        if 'prefill' in request.GET:
            try:
                existing_job = Job.objects.get(pk=request.GET['prefill'])
            except Job.DoesNotExist:
                raise Http404
            if existing_job.owner != request.user:
                raise PermissionDenied
            initial = {'name': (existing_job.name or 'Unnamed') + ' copy',
                       'reference': existing_job.reference,
                       'options': existing_job.options}
            form = JobForm(initial=initial)
        else:
            form = JobForm()
    return render(request, 'scheduler/create.html', {'form': form})


@login_required
def create_aligner(request, aligner):
    try:
        return render(request, 'scheduler/aligners/{}.html'.format(aligner))
    except TemplateDoesNotExist:
        raise Http404


@login_required
def create_aligner_container(request):
    return render(request, 'scheduler/create_aligner_container.html',
                  {'aligners': aligners})


@login_required
def delete(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        raise Http404
    if job.owner != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        job.deleted = True
        job.save()
        return HttpResponseRedirect(reverse('scheduler:index'))
    return render(request, 'scheduler/delete.html', {'job': job})


@login_required
def undelete(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        raise Http404
    if job.owner != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        job.deleted = False
        job.save()
        return HttpResponseRedirect(reverse('scheduler:detail', args=[pk]))
    return render(request, 'scheduler/undelete.html', {'job': job})


@login_required
def detail(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        raise Http404
    if job.owner != request.user:
        raise PermissionDenied
    with open(os.path.join(job.reference, 'genome.len')) as f:
        reference_length = int(f.read())
    return render(request, 'scheduler/detail.html',
                  {'job': job, 'reference_length': reference_length})


@login_required
def index(request):
    show_deleted = 'show_deleted' in request.GET
    jobs = Job.objects.filter(owner=request.user)
    if not show_deleted:
        jobs = jobs.filter(deleted=False)
    return render(request, 'scheduler/index.html',
                  {'jobs': jobs.order_by('-created_at'),
                   'show_deleted': show_deleted})


@login_required
def home(request):
    return render(request, 'scheduler/home.html')
