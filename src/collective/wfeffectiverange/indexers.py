# -*- coding: utf-8 -*-
from .behaviors import IWFEffectiveRange
from Acquisition import aq_base
from plone.indexer import indexer


@indexer(IWFEffectiveRange)
def has_effective_transition(context):
    context = aq_base(context)
    return bool(context.effective_transition)


@indexer(IWFEffectiveRange)
def has_expires_transition(context):
    context = aq_base(context)
    return bool(context.expires_transition)
