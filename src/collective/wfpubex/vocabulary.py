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


_ = MessageFactory('plone')



@implementer(IVocabularyFactory)
class PossibleTransitionsVocabulary(object):

    def __call__(self, context):

        portal = api.portal.get()

        # workflowtool

        import ipdb;

        ipdb.set_trace()
        wftool = api.portal.get_tool('portal_workflow')

        # da spinnts no rum
        context = aq_get(wftool, 'REQUEST', None)

        # get current state for context
        state = api.content.get_state(context)

        # get workflow for context.
        # we always get the first worklow - no implementation for multiple wfs


        wf = wftool.getWorkflowsFor(context)[0]

        # get possible transitions for this state
        transitions = wf.states[state].transitions

        terms = []

        for transition in transitions:
            # import ipdb;ipdb.set_trace()
            trans_id = wf.transitions[transition].id
            trans_title = wf.transitions[transition].title

            terms.append(SimpleVocabulary.createTerm(trans_id, trans_title))


        return SimpleVocabulary(terms)

PossibleTransitionsVocabularyFactory = PossibleTransitionsVocabulary()



#     def __call__(self, context):
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
# PossibleTransitionsVocabularyFactory = PossibleTransitionsVocabulary()
