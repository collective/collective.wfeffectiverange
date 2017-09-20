from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask
from DateTime import DateTime
from Products.CMFPlone.utils import safe_callable


def is_wfeffectiverange(ob):
    """True, if the object has the IWFEffectiveRange behavior.
    """
    return bool(IWFEffectiveRange(ob, False))


def is_task(ob):
    """True, if the object provides the IWFTask behavior interface.
    """
    return IWFTask.providedBy(ob)


def get_pub_date(it, type_):
    """Return the publication date without breaking into pieces.
    Once, expires was None and ExpirationDate returned the correct string.
    """
    pub = IWFEffectiveRange(it, None)
    if not pub:
        return
    return getattr(pub, type_, None)


def set_pub_date(it, type_, val):
    """Return the publication date without breaking into pieces.
    Once, expires was None and ExpirationDate returned the correct string.
    """
    pub = IWFEffectiveRange(it, None)
    if not pub:
        return
    return setattr(pub, type_, val)
