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




