from plone.indexer import indexer
from .behaviors import IPubexBehavior
from Acquisition import aq_base

@indexer(IPubexBehavior)
def has_eff_transition(context):
    context = aq_base(context)
    return bool(context.eff_transition)

@indexer(IPubexBehavior)
def has_exp_transition(context):
    context = aq_base(context)
    return bool(context.exp_transition)
