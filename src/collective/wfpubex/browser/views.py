# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder

class PubexView(BrowserView):

    def __call__(self):
        return ""




        # for trans in state.transitions:
        # state_to_trans.append((state.getId(), trans))

        # evtl für später
        #
        # uuid = api.content.get_uuid(self.context)
        # states = wf.states.values()
        #
        # do_trans = api.content.transition(obj=portal['about'],
        #                                transition='publish')
