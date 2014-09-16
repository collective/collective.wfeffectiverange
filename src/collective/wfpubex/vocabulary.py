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


@implementer(IVocabularyFactory)
class Transitions(object):
    def __call__(self, context):
        # workflowtool
        wftool = api.portal.get_tool('portal_workflow')

        url = context.REQUEST.getURL()

        # get workflow for already created content /on creating get workflow for this type

        #new content
        if '++add++' in url:
            # get the portal type from the url, because initial, self context is the vocab obj ;/
            # the part after the ++add++ is our portal_type aka context
            portal_type = re.split('.*\+{2}add\+{2}', url)[1]

            # get current state for portal_type
            # If it is given as a string it returns the default state. see PLIP 217 Workflow by adaptation
            state = api.content.get_state(portal_type)

        #editing content
        else:
            #import ipdb; ipdb.set_trace()
            state = api.content.get_state(context)
            portal_type = context.portal_type

        # get workflow for context.
        # TODO: if no workflow abfangen, und im behavior transitions ausschalten
        # we always get the first worklow - no implementation for multiple wfs
        wf = wftool.getWorkflowsFor(portal_type)[0]

        # get possible transitions for this state
        transitions = wf.states[state].transitions

        terms = []

        for transition in transitions:
            trans_id = wf.transitions[transition].id
            trans_title = wf.transitions[transition].title

            terms.append(SimpleVocabulary.createTerm(trans_id, trans_title))

        return SimpleVocabulary(terms)

TransitionsFactory = Transitions()



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
