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
    date = None
    if type_ == 'effective':
        date = getattr(it, 'EffectiveDate', None)
    elif type_ == 'expires':
        date = getattr(it, 'ExpirationDate', None)

    if safe_callable(date):
        date = date()

    return DateTime(date)
