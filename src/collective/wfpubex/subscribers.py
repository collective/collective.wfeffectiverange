from plone import api
from zExceptions import Redirect


def handle_workflow_change_before(event):
    context = event.object
    if (hasattr(context, 'eff_transition') and context.eff_transition) \
        or (hasattr(context, 'exp_transition') and context.exp_transition):
        api.portal.show_message(
            message="New workflow transition can't be set, because there is "
                    "already an automatic transition set.",
             request=context.REQUEST
        )
        raise(Redirect(context.absolute_url()))
