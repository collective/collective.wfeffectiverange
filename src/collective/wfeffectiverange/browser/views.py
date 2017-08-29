# -*- coding: utf-8 -*-
from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask
from collective.wfeffectiverange.vocabulary import ExpiresTransitionSource
from datetime import datetime
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import json
import logging
import plone.api
import plone.app.event


logger = logging.getLogger('wfeffectiverange')


class WFEffectiveRangeVocabReloadView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        transitions = ExpiresTransitionSource(
            transition=self.request.get('current'),
            portal_type=self.request.get('contenttype', None),
        )
        vocab = transitions(self.context)
        data = []

        for term in vocab:
            rekord = {}
            rekord['token'] = term.token
            rekord['title'] = term.title
            data.append(rekord)

        self.request.response.setHeader('Content-type', 'application/json')
        return json.dumps(data)


# vocabulary get all items that have a pub_transition and
# where their pub date is in the past
class WFEffectiveRangeTicker(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        triggered_something = 0

        # for effective transition
        query = {
            'effective': {'query': datetime.now(), 'range': 'max'},
            'has_effective_transition': True,
            # 'object_provides': IWFEffectiveRange.__identifier__
        }
        for brain in plone.api.content.find(**query):
            obj = brain.getObject()
            if getattr(obj, 'effective_transition', None):
                new_transition = obj.effective_transition
                obj.effective_transition = None
                obj._v_wfeffectiverange_ignore = True
                plone.api.content.transition(
                    obj=obj, transition=new_transition
                )
                obj._v_wfeffectiverange_ignore = False
                obj.reindexObject()
                logger.info(
                    'autotransition "effective" for {0}'.format(
                        obj.absolute_url()
                    )
                )
                triggered_something += 1

        # for expires transition
        query = {
            'expires': {'query': datetime.now(), 'range': 'max'},
            'has_expires_transition': True,
            # 'object_provides': IWFEffectiveRange.__identifier__
        }
        for brain in plone.api.content.find(**query):
            obj = brain.getObject()
            if hasattr(obj, 'expires_transition') and obj.expires_transition:
                new_transition = obj.expires_transition
                obj.expires_transition = None
                obj._v_wfeffectiverange_ignore = True
                plone.api.content.transition(
                    obj=obj, transition=new_transition
                )
                obj._v_wfeffectiverange_ignore = False
                obj.reindexObject()
                logger.info(
                    'autotransition "expires" for {0}'.format(
                        obj.absolute_url())
                )
                triggered_something += 1

        if not triggered_something:
            logger.info('no autotransition done in this cycle')
        return 'triggered {0} autotransitions.'.format(triggered_something)

        # Run Tasks
        infos = []
        warnings = []
        # Use timezone'd now.
        now = plone.app.event.base.localized_now(self.context)
        query = {
            'start': {'query': now, 'range': 'max'},
            'object_provides': IWFTask.__identifier__
        }
        for brain in plone.api.content.find(**query):
            task = brain.getObject()
            infos_, warnings_ = run_task(task, include_wfer=False)
            infos += infos_
            warnings += warnings_


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
