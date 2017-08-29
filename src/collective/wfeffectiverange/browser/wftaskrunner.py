# -*- coding: utf-8 -*-
# from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFEffectiveRange
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
    return bool(IWFEffectiveRange(ob, False))


def run_task(task, include_wfer=False, wftype=None):
    """Run a task.
    """
    infos = []
    warnings = []

    items = []

    if wftype:
        # If wftype is given - say that a IWFEffectiveRange "task" is run
        # manually - one of the following wftypes must be given.
        assert wftype in ('effective', 'expires')

    # Can also be run from an IWFEffectiveRange object instead of an IWFTask
    is_task = IWFTask.providedBy(task)

    if is_task:
        items = [it.to_object for it in getattr(task, 'task_items', [])]
    elif is_wfeffectiverange(task):
        items = [task]

    for obj in items:
        is_wfer = is_wfeffectiverange(obj)

        if not obj:
            # Invalid
            continue
        if not include_wfer and is_wfer:
            # WFEffectiveRange objects referenced by a task will get
            # multi-edited by the task and run individually via the
            # code above.
            # Do not run them again.
            continue

        transition = None
        if is_task:
            transition = getattr(task, 'task_transition', None)
        elif is_wfeffectiverange and wftype:
            transition = getattr(
                IWFEffectiveRange(obj, None),
                wftype + '_transition',
                None
            )
        if not transition:
            # Incomplete
            continue

        try:
            if is_wfer and include_wfer:
                obj._v_wfeffectiverange_ignore = True
            plone.api.content.transition(
                obj=obj,
                transition=transition
            )
            if is_wfer and include_wfer:
                obj._v_wfeffectiverange_ignore = True
                if wftype == 'effective'\
                        or task.portal_type == 'WFTaskEffective':
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
                transition,
                obj.absolute_url(),
                obj.title
            ))
            logger.warn(warnings[-1])

    if IWFTask.providedBy(task):
        # After running, clear the task transition and date.
        IWFTask(task).task_transition = None
        IWFTask(task).task_date = None

    task.reindexObject()

    return infos, warnings


class WFTaskRunnerView(BrowserView):

    infos = []
    warnings = []

    def __call__(self, *args, **kwargs):
        alsoProvides(self.request, IDisableCSRFProtection)

        wftype = self.request.form.get('wftype', None)
        uuid = self.request.form.get('uuid', None)
        if not uuid:
            return
        task = uuidToObject(uuid)

        self.infos, self.warnings = run_task(
            task,
            include_wfer=True,
            wftype=wftype
        )

        return super(WFTaskRunnerView, self).__call__(*args, **kwargs)
