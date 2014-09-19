from plone import api
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
import re

_ = MessageFactory('plone')


@implementer(IContextSourceBinder)
class TransitionsSource(object):
    def __init__(self, fieldname, cur_transition=None, cur_contenttype=None):
        self.fieldname = fieldname
        self.cur_transition = cur_transition
        self.cur_contenttype = cur_contenttype

    def __call__(self, context):
        # workflowtool
        wftool = api.portal.get_tool('portal_workflow')
        url = context.REQUEST.getURL()
        addform = '++add++' in url

        #first get current portal type
        # if addform and not bool(self.cur_contenttype):
        if addform and self.cur_contenttype == None:
            #Todo: also in der view und im javascript bekomme ich den wert
            #cur_contenttype noch zurück, hier aber ist er kurz da dann nicht mehr :/
            #steh hier voll an sry

            # get the portal type from the url, because initial, self context
            # is the vocab obj
            # the part after the ++add++ is our portal_type

            #strip the /@@validate_field
            url = re.sub('\/@{2}.*', '', url)
            portal_type = re.split('.*\+{2}add\+{2}', url)[1]
            import ipdb;ipdb.set_trace()
            #da dazubaun?

        if addform and self.cur_contenttype != None:
            'blub'

        else:
            portal_type = context.portal_type

        wfs = wftool.getWorkflowsFor(portal_type)
        if len(wfs) == 0:
            return SimpleVocabulary([])
        elif len(wfs) > 1:
            raise ValueError(
                'Multiple Workflow are not supported.'
            )

        wf = wfs[0]

        # if no eff_transition is set get all possible transitions
        # for the exp_transition
        # if an eff_transition is set, only get the allowed transitions for
        # that
        if self.cur_transition is None \
                and not addform \
                and context.eff_transition is not None \
                and self.fieldname == 'exp_transition':
            self.cur_transition = context.eff_transition

        if self.cur_transition and self.cur_transition != '--NOVALUE--':
            state = wf.transitions[self.cur_transition].new_state_id
            # get current state for portal_type
            # If it is given as a string it returns the default state.
            # see PLIP 217 Workflow by adaptation
        elif addform:
            state = api.content.get_state(portal_type)
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
