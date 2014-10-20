# -*- coding: utf-8 -*-
from collective.wfeffectiverange import _
from plone import api
from zExceptions import Redirect


def handle_workflow_change_before(event):
    context = event.object
    if getattr(context, '_v_wfeffectiverange_ignore', False):
        return
    if (hasattr(context, 'effective_transition')
        and context.effective_transition) \
       or (hasattr(context, 'expires_transition')
           and context.expires_transition):
        api.portal.show_message(
            message=_(u"New workflow transition can't be set, because there "
                      u"was already an automatic transition set."),
            request=context.REQUEST
        )
        raise(Redirect(context.absolute_url()))
