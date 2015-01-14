# -*- coding: utf-8 -*-
from collective.wfeffectiverange.vocabulary import TransitionsSource
from datetime import datetime
from logging import getLogger
from plone import api
from Products.Five.browser import BrowserView
import json

logger = getLogger('wfeffectiverange')


class WFEffectiveRangeVocabReloadView(BrowserView):

    def __call__(self):
        transitions = TransitionsSource(
            'effective_transition',
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

        self.request.response.setHeader("Content-type", "application/json")
        return json.dumps(data)


# vocabulary hohlen alle mit pub date in vergangenheit und has(pub_transition)
class WFEffectiveRangeTicker(BrowserView):

    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')

        triggered_something = 0

        # for effective transition
        query = {
            'effective': {'query': datetime.now(), 'range': 'max'},
            'has_effective_transition': True,
            # 'object_provides': IWFEffectiveRange.__identifier__
        }

        results = catalog.searchResults(query)
        for brain in results:
            obj = brain.getObject()
            if hasattr(obj, 'effective_transition'):
                new_transition = obj.effective_transition
                obj.effective_transition = None
                obj._v_wfeffectiverange_ignore = True
                api.content.transition(obj=obj, transition=new_transition)
                obj._v_wfeffectiverange_ignore = False
                obj.reindexObject()
                logger.info(
                    'autotransition "effective" for {0}'.format(
                        obj.absolute_url())
                )
                triggered_something += 1

        # for expires transition
        query = {
            'expires': {'query': datetime.now(), 'range': 'max'},
            'has_expires_transition': True,
            # 'object_provides': IWFEffectiveRange.__identifier__
        }

        results = catalog.searchResults(query)

        for brain in results:
            obj = brain.getObject()
            if hasattr(obj, 'expires_transition'):
                new_transition = obj.expires_transition
                obj.expires_transition = None
                obj._v_wfeffectiverange_ignore = True
                api.content.transition(obj=obj, transition=new_transition)
                obj._v_wfeffectiverange_ignore = False
                obj.reindexObject()
                logger.info(
                    'autotransition "expires" for {0}'.format(obj.absolute_url()))
                triggered_something += 1

        if not triggered_something:
            logger.info('no autotransition done in this cycle')

        return 'triggered {0} autotransitions.'.format(triggered_something)
