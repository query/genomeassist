from __future__ import division

import celery.states
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


STATE_CLASSES = {
    celery.states.PENDING: 'primary',
    celery.states.STARTED: 'warning',
    celery.states.SUCCESS: 'success',
    celery.states.FAILURE: 'danger',
}

@register.filter
def state_class(state):
    return STATE_CLASSES.get(state, 'muted')


@register.filter
def time(datetime):
    return mark_safe('<time datetime="{0}">{0}</time>'
                     .format(datetime.isoformat()))


@register.simple_tag
def ratio(numerator, denominator, percentage=False):
    r = min(float(numerator) / float(denominator), 1)
    if percentage:
        return r * 100
    return r
