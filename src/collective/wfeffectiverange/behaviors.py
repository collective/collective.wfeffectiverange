# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from collective.wfeffectiverange import _
from collective.wfeffectiverange.vocabulary import EffectiveTransitionSource
from collective.wfeffectiverange.vocabulary import ExpiresTransitionSource
from datetime import datetime
from plone.app.dexterity.behaviors import metadata
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component.hooks import getSite
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


@provider(IFormFieldProvider)
class IWFEffectiveRange(metadata.IPublication):
    """Workflow based publication and expiration
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

    # @invariant
    # def effective_and_effective_transition(data):
    #     if data.effective is not None \
    #        and data.effective > datetime.now() \
    #        and data.effective_transition is None:
    #         raise Invalid(_(u'If a publication date is set, '
    #                         u'a publication transition is needed.'))

    # @invariant
    # def expires_and_expires_transition(data):
    #     if data.expires is not None \
    #        and data.expires > datetime.now()\
    #        and data.expires_transition is None:
    #         raise Invalid(_(u'If a expiration date is set, '
    #                         u'a expiration transition is needed.'))

    # @invariant
    # def effective_transition_without_effective(data):
    #     if data.effective is None and data.effective_transition is not None:
    #         raise Invalid(_(u'If a publication transition is set, '
    #                         u'a publication date is needed.'))

    # @invariant
    # def expires_transition_without_expires(data):
    #     if data.expires is None and data.expires_transition is not None:
    #         raise Invalid(_(u'If a expiration date is set, '
    #                         u'a expiration transition is needed.'))


class WFEffectiveRange(metadata.Publication):

    effective_transition = metadata.DCFieldProperty(
        IWFEffectiveRange['effective_transition']
    )

    expires_transition = metadata.DCFieldProperty(
        IWFEffectiveRange['expires_transition']
    )


@provider(IFormFieldProvider)
class IWFTask(model.Schema):
    """Behavior providing fields for the workflow tasks.
    """

    task_items = RelationList(
        title=_(
            u'label_task_items',
            default=u'Task items'
        ),
        description=_(
            u'description_task_items',
            default=u'Select one or more content objects to be processed.'
        ),
        default=[],
        value_type=RelationChoice(
            title=_(u'label_task_items', default=u'Task items'),
            vocabulary='plone.app.vocabularies.Catalog',
        ),
        required=True,
    )
    form.widget(
        'task_items',
        RelatedItemsFieldWidget,
        pattern_options={
            'basePath': lambda ctx: '/'.join(getSite().getPhysicalPath())
        }
    )

    task_transition = schema.Choice(
        title=_(
            u'label_task_transition',
            default=u'Task action'),
        description=_(
            u'help_task_transition',
            default=u'Select a workflow transition, which should be applied '
                    u'when the task is executed.',
        ),
        vocabulary='plone.app.vocabularies.WorkflowTransitions',
        required=True,
        missing_value='',
    )
    form.widget(
        'task_transition',
        SelectFieldWidget
    )

    task_date = schema.Datetime(
        title=_(
            u'label_task_date',
            default=u'Task task date'
        ),
        description=_(
            u'help_task_date',
            default=u'Date and time, when the task action should be executed.'
        ),
        required=False,
        default=None
    )
    form.widget(
        'task_date',
        DatetimeFieldWidget
    )

    form.omitted('task_transition', 'task_date')
