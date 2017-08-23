# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.indexer import indexer
from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask


@indexer(IWFEffectiveRange)
def has_effective_transition(context):
    context = aq_base(context)
    return hasattr(context, 'effective_transition')\
        and bool(context.effective_transition)


@indexer(IWFEffectiveRange)
def has_expires_transition(context):
    context = aq_base(context)
    return hasattr(context, 'expires_transition')\
        and bool(context.expires_transition)


@indexer(IWFTask)
def date_indexer(obj):
    acc = IWFTask(obj, None)
    date = acc.task_date
    if not date:
        raise AttributeError
    return date
