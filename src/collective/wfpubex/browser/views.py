# -*- coding: utf-8 -*-
from collective.wfpubex.behaviors import IPubexBehavior
from collective.wfpubex.vocabulary import TransitionsSource
from datetime import datetime
from logging import getLogger
from plone import api
from Products.Five.browser import BrowserView
import json

logger = getLogger('pubex')


class PubexView(BrowserView):

    def __call__(self):
        transitions = TransitionsSource(
            'effective_transition',
            cur_transition=self.request.get('current'),
            cur_contenttype=self.request.get('contenttype'),
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
class PubexTicker(BrowserView):

    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')

        # for effective transition
        query = {'effective': {'query': datetime.now(), 'range': 'max'},
                 'has_effective_transition': True,
                 'object_provides': IPubexBehavior.__identifier__}

        results = catalog.searchResults(query)

        for brain in results:
            obj = brain.getObject()
            new_transition = obj.effective_transition
            obj.effective_transition = None
            api.content.transition(obj=obj, transition=new_transition)
            obj.reindexObject()
            logger.info(
                'autotransition effective for {0}'.format(obj.absolute_url()))

        #for expires transition
        query = {'expires': {'query': datetime.now(), 'range': 'max'},
                 'has_expires_transition': True,
                 'object_provides': IPubexBehavior.__identifier__}

        results = catalog.searchResults(query)

        for brain in results:
            obj = brain.getObject()
            new_transition = obj.expires_transition
            obj.expires_transition = None
            api.content.transition(obj=obj, transition=new_transition)
            obj.reindexObject()
            logger.info(
                'autotransition expires for {0}'.format(obj.absolute_url()))
