# -*- coding: utf-8 -*-
from collective.wfeffectiverange.behaviors import IWFTask
from collective.wfeffectiverange.browser.wftaskrunner import run_task
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
                plone.api.content.transition(obj=obj, transition=new_transition)
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
                plone.api.content.transition(obj=obj, transition=new_transition)
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
