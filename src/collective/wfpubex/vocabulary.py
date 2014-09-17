from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder

from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite
from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Acquisition import aq_get
import re
from persistent import Persistent


_ = MessageFactory('plone')


@implementer(IContextSourceBinder)
class TransitionsSource(object):
    def __init__(self, fieldname, cur_transition=None):
        self.fieldname = fieldname
        self.cur_transition = cur_transition

    def __call__(self, context):
        # workflowtool
        wftool = api.portal.get_tool('portal_workflow')
        url = context.REQUEST.getURL()
        addform = '++add++' in url

        # first get current portal type
        if addform:
            # get the portal type from the url, because initial, self context is the vocab obj ;/
            # the part after the ++add++ is our portal_type aka context
            portal_type = re.split('.*\+{2}add\+{2}', url)[1]
        else:
            portal_type = context.portal_type

        # get workflow for context.
        #  TODO: if no workflow abfangen, und im behavior transitions ausschalten
        # we always get the first worklow - no implementation for multiple wfs
        wf = wftool.getWorkflowsFor(portal_type)[0]

        # if no eff_transition is set get all possible transitions for exp_transition
        # if an eff_transition is set, only get the allowed transitions for that
        if self.cur_transition is None\
           and not addform \
           and context.eff_transition is not None \
           and self.fieldname == 'exp_transition':
            self.cur_transition = context.eff_transition

        if self.cur_transition:
            state = wf.transitions[self.cur_transition].new_state_id
            # get current state for portal_type
            # If it is given as a string it returns the default state. see PLIP 217 Workflow by adaptation
        elif addform:
            state = api.content.get_state(portal_type)
        else:
            state = api.content.get_state(context)

            #future state, for the exp_transitions dropdown


        # get possible transitions for this state
        transitions = wf.states[state].transitions


        terms = []

        for transition in transitions:
            trans_id = wf.transitions[transition].id
            #todo shortname
            trans_title = wf.transitions[transition].title

            terms.append(SimpleVocabulary.createTerm(trans_id, trans_id, trans_title))

        return SimpleVocabulary(terms)





# def __call__(self, context):
#         site = getSite()
#         wtool = getToolByName(site, 'portal_workflow', None)
#
#
#
#         transitions = {}
#         for wf in wtool.values():
#             transition_folder = getattr(wf, 'transitions', None)
#
#             wf_name = wf.title or wf.id
#             if transition_folder is not None:
#                 for transition in transition_folder.values():
#                     name = safe_unicode(transition.actbox_name)
#                     transition_title = translate(
#                         _(name),
#                         context=aq_get(wtool, 'REQUEST', None))
#
#                     transitions.setdefault(transition.id, []).append(
#                         dict(title=transition_title, wf_name=wf_name))
#
#         items = []
#         transition_items = transitions.items()
#         transition_items.sort(key=lambda transition: transition[0])
#         for transition_id, info in transition_items:
#             titles = set([i['title'] for i in info])
#             item_title = ' // '.join(sorted(titles))
#             item_title = "%s [%s]" % (item_title, transition_id)
#             items.append(SimpleTerm(transition_id, transition_id, item_title))
#
#         return SimpleVocabulary(items)
#
#
# TransitionsFactory = Transitions()
