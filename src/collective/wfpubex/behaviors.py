# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from collective.wfpubex import _
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider
from plone.app.dexterity.behaviors.metadata import IPublication
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.autoform import directives as form
from z3c.form.interfaces import IEditForm, IAddForm
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
