# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer


@indexer(IDexterityContent)
def has_effective_transition(context):
    context = aq_base(context)
    return hasattr(context, 'effective_transition')\
        and bool(context.effective_transition)


@indexer(IDexterityContent)
def has_expires_transition(context):
    context = aq_base(context)
    return hasattr(context, 'expires_transition')\
        and bool(context.expires_transition)
