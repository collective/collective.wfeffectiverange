# -*- coding: utf-8 -*-
from plone import api
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
import re

_ = MessageFactory('plone')


@implementer(IContextSourceBinder)
class TransitionsSource(object):

    def __init__(self, fieldname, transition=None, portal_type=None):
        self.fieldname = fieldname
        self.transition = transition
        self.portal_type = portal_type

    def __call__(self, context):
        # workflowtool
        wftool = api.portal.get_tool('portal_workflow')
        url = context.REQUEST.getURL()
        addform = '++add++' in url

        if self.portal_type is None:
            if addform:
                # todo: could be done in one step with re.match.
                # strip the /@@validate_field!
                url = re.sub('\/@{2}.*', '', url)
                # get portal_type from addform
                self.portal_type = re.split('.*\+{2}add\+{2}', url)[1]
            else:
                self.portal_type = context.portal_type

        wfs = wftool.getWorkflowsFor(self.portal_type)
        if len(wfs) == 0:
            return SimpleVocabulary([])
        elif len(wfs) > 1:
            raise ValueError(
                _(u'Multiple workflows are not supported.')
            )

        wf = wfs[0]

        # if no effective_transition is set get all possible transitions
        # for the expires_transition
        # if an effective_transition is set, only get the allowed
        # transitions for that
        if self.transition is None \
                and not addform \
                and context.effective_transition is not None \
                and self.fieldname == 'expires_transition':
            self.transition = context.effective_transition

        if self.transition and self.transition != '--NOVALUE--':
            state = wf.transitions[self.transition].new_state_id
            # get current state for portal_type
            # If it is given as a string it returns the default state.
            # see PLIP 217 Workflow by adaptation
        elif addform:
            state = api.content.get_state(self.portal_type)
        else:
            state = api.content.get_state(context)

        # get possible transitions for this state
        transitions = wf.states[state].transitions
        terms = []

        for transition in transitions:
            trans_id = wf.transitions[transition].id
            terms.append(
                SimpleVocabulary.createTerm(trans_id, trans_id, trans_id))

        return SimpleVocabulary(terms)
