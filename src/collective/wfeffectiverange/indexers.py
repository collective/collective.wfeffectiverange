# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.indexer import indexer
from plone.dexterity.interfaces import IDexterityContent
from collective.wfeffectiverange.behaviors import IWFTask


@indexer(IDexterityContent)
def has_effective_transition(context):
    context = aq_base(context)
    return bool(getattr(context, 'effective_transition', False))


@indexer(IDexterityContent)
def has_expires_transition(context):
    context = aq_base(context)
    return bool(getattr(context, 'expires_transition', False))


@indexer(IWFTask)
def date_indexer(obj):
    acc = IWFTask(obj, None)
    date = acc.task_date
    if not date:
        raise AttributeError
    return date
