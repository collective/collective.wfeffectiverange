# -*- coding: utf-8 -*-
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from collective.wfpubex import _
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider
from plone.app.dexterity.behaviors.metadata import IPublication
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.autoform import directives as form
from z3c.form.interfaces import IEditForm, IAddForm
from plone.autoform.form import AutoExtensibleForm
from zope.interface import alsoProvides
from plone.fieldsets.fieldsets import FormFieldsets
from collective.wfpubex.vocabulary import TransitionsSource

@provider(IFormFieldProvider)
class IPubexBehavior(IPublication):
    """
    workflow based publication and expiration
    """
    model.fieldset(
        'dates',
        label=_PMF(u'label_schema_dates', default=u'Dates'),
        fields=['eff_transition', 'exp_transition'],
    )

    form.order_after(eff_transition='effective')
    eff_transition = schema.Choice(
        title=_(u"Publication Transition"),
        description=_(u"Required if a publishing date is set"),
        source=TransitionsSource('eff_transition'),
        required=False
    )

    form.order_after(exp_transition='expires')
    exp_transition = schema.Choice(
        title=_(u"Expiration Transition"),
        description=_(u"Required if a expiration date is set"),
        source=TransitionsSource('exp_transition'),
        required=False
    )

    form.omitted('eff_transition', 'exp_transition')
    form.no_omit(IEditForm, 'eff_transition', 'exp_transition')
    form.no_omit(IAddForm, 'eff_transition', 'exp_transition')

    @invariant
    def effective_and_eff_transition(data):
        if data.effective is not None and data.eff_transition is None:
            raise Invalid(_(u"If a publication date is set, "
                            u"a publication transition is needed."))

    @invariant
    def expires_and_exp_transition(data):
        if data.expires is not None and data.exp_transition is None:
            raise Invalid(_(u"If a expiration date is set, "
                            u"a expiration transition is needed."))

    @invariant
    def eff_transition_without_effective(data):
        if data.effective is None and data.eff_transition is not None:
            raise Invalid(_(u"If a publication transition is set, "
                            u"a publication date is needed."))

    @invariant
    def exp_transition_without_expires(data):
        if data.expires is None and data.exp_transition is not None:
            raise Invalid(_(u"If a expiration date is set, "
                            u"a expiration transition is needed."))


# @provider(IFormFieldProvider)
# class IPubexBehavior(IPublication):
#     """
#     workflow based publication and expiration
#     """
#
#     model.fieldset(
#             'dates',
#             label=_PMF(u'label_schema_dates', default=u'Dates'),
#             fields=['eff_transition', 'exp_transition'],
#         )
#
#     form.order_after(eff_transition='IPublication.effective')
#     eff_transition = schema.Choice(
#         title=_(u"Publication Transition"),
#         description=_(u"Required if a publishing date is set"),
#         # vocabulary="plone.app.vocabularies.SupportedContentLanguages",
#         values=['publish', 'submit for pub', 'nochwas'],
#         required=False
#     )
#
#     form.order_after(exp_transition='IPublication.expires')
#     exp_transition = schema.Choice(
#         title=_(u"Expiration Transition"),
#         description=_(u"Required if a expiration date is set"),
#         values=['private', 'retreat', 'regret'],
#         required=False
#     )
#
#     form.omitted('eff_transition', 'exp_transition')
#     form.no_omit(IEditForm, 'eff_transition', 'exp_transition')
#     form.no_omit(IAddForm, 'eff_transition', 'exp_transition')
#     model.fieldset('dates','dat')
# #
# # class MySimpleForm:
# #     form_fields = FormFieldsets(IPubexBehavior, IPublication)
#




# class IPublication(model.Schema):
# # dates fieldset
#     model.fieldset(
#         'dates',
#         label=_PMF(u'label_schema_dates', default=u'Dates'),
#         fields=['effective', 'expires'],
#     )
#
#     effective = schema.Datetime(
#         title=_PMF(u'label_effective_date', u'Publishing Date'),
#         description=_PMF(
#             u'help_effective_date',
#             default=u"If this date is in the future, the content will "
#                     u"not show up in listings and searches until this date."),
#         required=False
#     )
#
#     expires = schema.Datetime(
#         title=_PMF(u'label_expiration_date', u'Expiration Date'),
#         description=_PMF(
#             u'help_expiration_date',
#             default=u"When this date is reached, the content will no"
#                     u"longer be visible in listings and searches."),
#         required=False
#     )
#
#     form.omitted('effective', 'expires')
#     form.no_omit(IEditForm, 'effective', 'expires')
#     form.no_omit(IAddForm, 'effective', 'expires')
