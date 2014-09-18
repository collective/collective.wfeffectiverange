# -*- coding: utf-8 -*-
from collective.wfpubex.vocabulary import TransitionsSource
from Products.Five.browser import BrowserView
import json
from plone import api
from logging import getLogger
logger = getLogger('pubex')
from  datetime import datetime

class PubexView(BrowserView):
    def __call__(self):
        transitions = TransitionsSource(
            'eff_transition',
            cur_transition=self.request.get('current')
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


#>>> client.set_workflow('publish', 'weblion')
#>> > client.get_workflow('weblion')
#{'state': 'published', 'transitions': ['retract', 'reject']}

# vocabulary hohlen alle mit pub date in vergangenheit und has(pub_transition)
class PubexTicker(BrowserView):
    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')
        wftool = api.portal.get_tool('portal_workflow')

        query = {'effective': {'query': [datetime.now,],'range':'max'},
                 'has_eff_transition': 'True',
                 'object_provides': 'IPubexBehavior.__identifier__',}

        import ipdb; ipdb.set_trace()
        results = catalog.searchResults(query)

        for brain in results:
            'foo'


        logger.info('foo')
