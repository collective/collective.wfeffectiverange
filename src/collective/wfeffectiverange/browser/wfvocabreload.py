# -*- coding: utf-8 -*-
from collective.wfeffectiverange.vocabulary import ExpiresTransitionSource
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import json


# vocabulary get all items that have a pub_transition and
# where their pub date is in the past
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
