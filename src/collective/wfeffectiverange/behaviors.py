# -*- coding: utf-8 -*-
from collective.wfeffectiverange import _
from collective.wfeffectiverange.vocabulary import EffectiveTransitionSource
from collective.wfeffectiverange.vocabulary import ExpiresTransitionSource
from datetime import datetime
from plone.app.dexterity.behaviors import metadata
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


@provider(IFormFieldProvider)
class IWFEffectiveRange(metadata.IPublication):
    """
    workflow based publication and expiration
    """
    model.fieldset(
        'dates',
        label=_(u'label_schema_dates', default=u'Dates'),
        fields=['effective_transition', 'expires_transition'],
    )

    # form.order_after(effective_transition='IPublication.effective')
    effective_transition = schema.Choice(
        title=_(u'Publication Transition'),
        description=_(u'Required if a publishing date is set'),
        source=EffectiveTransitionSource(),
        required=False,
        default=None,
    )

    # form.order_after(expires_transition='IPublication.expires')
    expires_transition = schema.Choice(
        title=_(u'Expiration Transition'),
        description=_(u'Required if a expiration date is set'),
        source=ExpiresTransitionSource(),
        required=False,
        default=None,
    )

    form.omitted('effective_transition', 'expires_transition')
    form.no_omit(IEditForm, 'effective_transition', 'expires_transition')
    form.no_omit(IAddForm, 'effective_transition', 'expires_transition')

    @invariant
    def effective_and_effective_transition(data):
        if data.effective is not None \
           and data.effective > datetime.now() \
           and data.effective_transition is None:
            raise Invalid(_(u'If a publication date is set, '
                            u'a publication transition is needed.'))

    @invariant
    def expires_and_expires_transition(data):
        if data.expires is not None \
           and data.expires > datetime.now()\
           and data.expires_transition is None:
            raise Invalid(_(u'If a expiration date is set, '
                            u'a expiration transition is needed.'))

    @invariant
    def effective_transition_without_effective(data):
        if data.effective is None and data.effective_transition is not None:
            raise Invalid(_(u'If a publication transition is set, '
                            u'a publication date is needed.'))

    @invariant
    def expires_transition_without_expires(data):
        if data.expires is None and data.expires_transition is not None:
            raise Invalid(_(u'If a expiration date is set, '
                            u'a expiration transition is needed.'))


class WFEffectiveRange(metadata.Publication):

    effective_transition = metadata.DCFieldProperty(
        IWFEffectiveRange['effective_transition']
    )

    expires_transition = metadata.DCFieldProperty(
        IWFEffectiveRange['expires_transition']
    )
