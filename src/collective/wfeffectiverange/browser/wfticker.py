# -*- coding: utf-8 -*-
from collective.wfeffectiverange import utils
from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask
from datetime import datetime
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides

import logging
import plone.api
import transaction


logger = logging.getLogger('wfeffectiverange')
WFTASK_LOGGER_KEY = 'wftasklogger'


def run_task(task, include_wfer=False, wftype=None):
    """Run a IWFTask.
    """
    infos = []
    warnings = []

    if wftype:
        # If wftype is given - say that a IWFEffectiveRange "task" is run
        # manually - one of the following wftypes must be given.
        assert wftype in ('effective', 'expires')

    items = []
    is_task = utils.is_task(task)
    if is_task:
        items = [it.to_object for it in getattr(task, 'task_items', [])]
    elif utils.is_wfeffectiverange(task):
        items = [task]

    for obj in items:
        is_wfer = utils.is_wfeffectiverange(obj)

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
        elif is_wfer and wftype:
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
            infos.append(u'Task {0} successfully run for object {1}.'.format(
                task.title,
                obj.title
            ))
            logger.info(infos[-1])

        except plone.api.exc.InvalidParameterError:
            warnings.append(u'Could not apply task {0} with transform {1} for object {2}.'.format(  # noqa
                task.title,
                transition,
                obj.title
            ))
            logger.warn(warnings[-1])

    if IWFTask.providedBy(task):
        # After running, clear the task transition and date.
        IWFTask(task).task_transition = None
        IWFTask(task).task_date = None

    annotations = IAnnotations(task)
    tasklogger = annotations.get(WFTASK_LOGGER_KEY, {})
    tasklogger[datetime.now().isoformat()] = {
        'infos': infos,
        'warnings': warnings
    }
    annotations[WFTASK_LOGGER_KEY] = tasklogger

    task.reindexObject()

    return infos, warnings


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
                try:
                    plone.api.content.transition(
                        obj=obj, transition=new_transition
                    )
                except plone.api.exc.InvalidParameterError as e:
                    logger.warn(u'Error on running effective transition on object {0}'.format(  # noqa
                        obj.absolute_url()
                    ))
                    raise e
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
                try:
                    plone.api.content.transition(
                        obj=obj, transition=new_transition
                    )
                except plone.api.exc.InvalidParameterError as e:
                    logger.warn(u'Error on running expires transition on object {0}'.format(  # noqa
                        obj.absolute_url()
                    ))
                    raise e
                obj._v_wfeffectiverange_ignore = False
                obj.reindexObject()
                logger.info(
                    'autotransition "expires" for {0}'.format(
                        obj.absolute_url())
                )
                triggered_something += 1

        # Run Tasks
        query = {
            'start': {'query': datetime.now(), 'range': 'max'},
            'object_provides': IWFTask.__identifier__
        }

        infos = []
        warnings = []

        for brain in plone.api.content.find(**query):
            task = brain.getObject()
            _infos, _warnings = run_task(task, include_wfer=False)
            infos += _infos
            warnings += _warnings

        transaction.commit()

        if not triggered_something:
            logger.info('no autotransition done in this cycle')
        return u'''Triggered {0} autotransitions.

Task infos
----------
{1}

Task warnings
-------------
{2}
'''.format(
            triggered_something,
            u'    {0}\n'.join(infos),
            u'    {0}\n'.join(warnings)
        )
