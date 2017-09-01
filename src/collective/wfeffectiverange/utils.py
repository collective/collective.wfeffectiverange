from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask


def is_wfeffectiverange(ob):
    """True, if the object has the IWFEffectiveRange behavior.
    """
    return bool(IWFEffectiveRange(ob, False))


def is_task(ob):
    """True, if the object provides the IWFTask behavior interface.
    """
    return IWFTask.providedBy(ob)
