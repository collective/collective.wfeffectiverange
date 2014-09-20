# -*- coding: utf-8 -*-
from plone.indexer import indexer
from .behaviors import IPubexBehavior
from Acquisition import aq_base


@indexer(IPubexBehavior)
def has_effective_transition(context):
    context = aq_base(context)
    return bool(context.effective_transition)


@indexer(IPubexBehavior)
def has_expires_transition(context):
    context = aq_base(context)
    return bool(context.expires_transition)
