# -*- coding: utf-8 -*-
# from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask
from plone.app.uuid.utils import uuidToObject
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import json
import logging
import plone.api
import plone.app.event


logger = logging.getLogger('wfeffectiverange')


def is_wfeffectiverange(ob):
    return getattr(ob, 'effective_transition', False) or\
        getattr(ob, 'expires_transition', False)


def run_task(task, include_wfer=False):
    """Run a task.
    """
    infos = []
    warnings = []

    for ref in task.task_items:
        obj = ref.to_object

        if not obj:
            # Invalid
            continue
        # if not include_wfer and IWFEffectiveRange.providedBy(obj):
        if not include_wfer and is_wfeffectiverange(obj):
            # WFEffectiveRange objects referenced by a task will get
            # multi-edited by the task and run individually via the
            # code above.
            # Do not run them again.
            continue

        transition = getattr(task, 'task_transition', None)
        if not transition:
            # Incomplete
            continue

        try:
            plone.api.content.transition(
                obj=obj,
                transition=transition
            )
            # if IWFEffectiveRange.providedBy(obj) and include_wfer:
            if is_wfeffectiverange(obj) and include_wfer:
                if task.portal_type == 'WFTaskEffective':
                    obj.effective_transition = None
                else:
                    obj.expires_transition = None
            obj.reindexObject()
            infos.append(u'Task <a href="{0}">{1}</a> successfully run for object <a href="{2}">{3}</a>.'.format(  # noqa
                task.absolute_url(),
                task.title,
                obj.absolute_url(),
                obj.title
            ))
            logger.info(infos[-1])

        except plone.api.exc.InvalidParameterError:
            warnings.append(u'Could not apply task <a href="{0}">{1}</a> with transform {2} for object <a href="{3}">{4}</a>.'.format(  # noqa
                task.absolute_url(),
                task.title,
                task.task_transition,
                obj.absolute_url(),
                obj.title
            ))
            logger.warn(warnings[-1])

    IWFTask(task).task_transition = None
    IWFTask(task).task_date = None
    task.reindexObject()

    return infos, warnings


class WFTaskRunnerView(BrowserView):

    infos = []
    warnings = []

    def __call__(self, *args, **kwargs):
        alsoProvides(self.request, IDisableCSRFProtection)
        
        task_uuid = self.request.form.get('task_uid', None)
        if not task_uuid:
            return

        task = uuidToObject(task_uuid)
        self.infos, self.warnings = run_task(task, include_wfer=True)

        return super(WFTaskRunnerView, self).__call__(*args, **kwargs)
