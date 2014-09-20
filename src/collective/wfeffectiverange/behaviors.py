# -*- coding: utf-8 -*-
from collective.wfeffectiverange import _
from collective.wfeffectiverange.vocabulary import TransitionsSource
from datetime import datetime
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.app.dexterity.behaviors import metadata
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IEditForm, IAddForm
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


@provider(IFormFieldProvider)
class IPubexBehavior(metadata.IPublication):
    """
    workflow based publication and expiration
    """
    model.fieldset(
        'dates',
        label=_PMF(u'label_schema_dates', default=u'Dates'),
        fields=['effective_transition', 'expires_transition'],
    )

    form.order_after(effective_transition='effective')
    effective_transition = schema.Choice(
        title=_(u"Publication Transition"),
        description=_(u"Required if a publishing date is set"),
        source=TransitionsSource('effective_transition'),
        required=False
    )

    form.order_after(expires_transition='expires')
    expires_transition = schema.Choice(
        title=_(u"Expiration Transition"),
        description=_(u"Required if a expiration date is set"),
        source=TransitionsSource('expires_transition'),
        required=False
    )

    form.omitted('effective_transition', 'expires_transition')
    form.no_omit(IEditForm, 'effective_transition', 'expires_transition')
    form.no_omit(IAddForm, 'effective_transition', 'expires_transition')

    @invariant
    def effective_and_effective_transition(data):
        if data.effective is not None \
           and data.effective > datetime.now() \
           and data.effective_transition is None:
            raise Invalid(_(u"If a publication date is set, "
                            u"a publication transition is needed."))

    @invariant
    def expires_and_expires_transition(data):
        if data.expires is not None \
           and data.expires > datetime.now()\
           and data.expires_transition is None:
            raise Invalid(_(u"If a expiration date is set, "
                            u"a expiration transition is needed."))

    @invariant
    def effective_transition_without_effective(data):
        if data.effective is None and data.effective_transition is not None:
            raise Invalid(_(u"If a publication transition is set, "
                            u"a publication date is needed."))

    @invariant
    def expires_transition_without_expires(data):
        if data.expires is None and data.expires_transition is not None:
            raise Invalid(_(u"If a expiration date is set, "
                            u"a expiration transition is needed."))


class IPubexDublinCore(metadata.IBasic,
                       metadata.ICategorization,
                       IPubexBehavior,
                       metadata.IOwnership):
    pass


# factories:
class Pubex(metadata.Publication):
    pass


class PubexDublingCore(metadata.Basic,
                       metadata.Categorization,
                       Pubex,
                       metadata.Ownership):
    pass
