# -*- coding: utf-8 -*-
from collective.wfeffectiverange import _
from plone import api
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

import re
import urllib

_pmf = MessageFactory('plone')


@implementer(IContextSourceBinder)
class BaseTransitionsSource(object):

    FIELD_NAME = ''

    def __init__(self):
        self.portal_type = None

    def _init_call(self, context):
        from .behaviors import WFEffectiveRange
        if isinstance(context, WFEffectiveRange):
            context = context.context
        url = urllib.unquote(context.REQUEST.getURL())
        addform = '++add++' in url
        addtranslationform = '++addtranslation++' in url
        self.add = addform or addtranslationform
        if self.portal_type is None:
            if addform:
                # todo: could be done in one step with re.match.
                # strip the /@@validate_field!
                self.url = re.sub('\/@{2}.*', '', url)
                # get portal_type from addform
                self.portal_type = re.split('.*\+{2}add\+{2}', url)[1]
            elif addtranslationform:
                self.url = re.sub('\/@{2}.*', '', url)
                # get portal_type from addform
                self.portal_type = re.split(
                    '.*\+{2}addtranslation\+{2}', url
                )[1]
            else:
                self.portal_type = context.portal_type
        wftool = api.portal.get_tool('portal_workflow')
        self.workflows = wftool.getWorkflowsFor(self.portal_type)
        self.submitted = context.REQUEST.form.get(self.FIELD_NAME, None)
        return context

    def _vocab_transitions(self, state):
        """get possible transitions for this state
        """
        transitions = self.workflow.states[state].transitions
        terms = []
        for transition in transitions:
            trans_id = self.workflow.transitions[transition].id
            terms.append(
                SimpleVocabulary.createTerm(
                    trans_id,
                    trans_id,
                    _pmf(trans_id)
                )
            )
        return SimpleVocabulary(terms)


class EffectiveTransitionSource(BaseTransitionsSource):

    def __call__(self, context):
        context = self._init_call(context)
        if len(self.workflows) == 0:
            return SimpleVocabulary([])
        elif len(self.workflows) > 1:
            raise ValueError(
                _(u'Multiple workflows are not supported.')
            )
        self.workflow = self.workflows[0]
        if self.add:
            # get current state for portal_type
            # If it is given as a string it returns the default state.
            # see PLIP 217 Workflow by adaptation
            state = api.content.get_state(self.portal_type)
        else:
            state = api.content.get_state(context)
        return self._vocab_transitions(state)


class ExpiresTransitionSource(BaseTransitionsSource):

    FIELD_NAME = 'form.widgets.IWFEffectiveRange.effective_transition'

    def __init__(self, transition=None, portal_type=None):
        self.transition = transition
        self.portal_type = portal_type

    def __call__(self, context):
        context = self._init_call(context)
        if len(self.workflows) == 0:
            return SimpleVocabulary([])
        elif len(self.workflows) > 1:
            raise ValueError(
                _(u'Multiple workflows are not supported.')
            )
        self.workflow = self.workflows[0]

        if self.transition == u'--NOVALUE--':
            self.transition = None

        if self.transition is None:
            if self.submitted and self.submitted[0] != u'--NOVALUE--':
                self.transition = self.submitted[0]
            elif not self.add:
                self.transition = getattr(
                    context,
                    'effective_transition',
                    None
                )
                if self.transition == u'--NOVALUE--':
                    self.transition = None
        if self.transition:
            state = self.workflow.transitions[self.transition].new_state_id
        elif self.add:
            # get current state for portal_type
            # If it is given as a string it returns the default state.
            # see PLIP 217 Workflow by adaptation
            state = api.content.get_state(self.portal_type)
        else:
            state = api.content.get_state(context)
        return self._vocab_transitions(state)
