# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
import json
from collective.wfpubex.vocabulary import TransitionsSource

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
