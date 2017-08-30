# -*- coding: utf-8 -*-
from collective.wfeffectiverange import _
from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask
from collective.wfeffectiverange.browser.views import run_task
from collective.wfeffectiverange.vocabulary import EffectiveTransitionSource
from collective.wfeffectiverange.vocabulary import ExpiresTransitionSource
from DateTime import DateTime
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.uuid.utils import uuidToObject
from plone.protect.utils import addTokenToUrl
from plone.uuid.interfaces import IUUID
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import plone.api


class WFTaskOverviewView(FolderView):

    @property
    def protected_view_url(self):
        url = addTokenToUrl(self.context.absolute_url() + '/@@wftaskoverview')
        return url

    def items(self, type_='effective'):

        intids = getUtility(IIntIds)
        wftool = plone.api.portal.get_tool('portal_workflow')

        ret_tasks = plone.api.content.find(**{
            'portal_type': 'WFTask' + type_.capitalize()
        })
        ret_tasks = [it.getObject() for it in ret_tasks]
        # Get all task_items ids for IWFEffectiveRange object filtering.
        task_items_ids = []
        for task in ret_tasks:
            task_items_ids += [it.to_id for it in task.task_items]

        ret_obj = plone.api.content.find(**{
            'has_' + type_ + '_transition': True
        })
        # Filter all IWFEffectiveRange objects, which are already related in an
        # IWFTask object.
        # Plus, filter out effective of 1969,30,12 and expires of 2499,30,12.
        # Add a little buffer for timezone quirks. You never know...
        # Also, get the object as we need it anyways.
        ret_obj = [
            it.getObject()
            for it in ret_obj
            if intids.getId(it.getObject()) not in task_items_ids
            and (
                (type_ == 'effective' and (
                    not getattr(it, 'effective', False)
                    or it.effective > DateTime(1970, 1, 2)
                )) or
                (type_ == 'expires' and (
                    not getattr(it, 'expires', False)
                    or it.expires < DateTime(2499, 1, 1)
                ))
            )
        ]

        def _datecomp(x, y):
            dat_x = getattr(x, 'task_date', getattr(IWFEffectiveRange(x, None), type_, None))  # noqa
            dat_y = getattr(y, 'task_date', getattr(IWFEffectiveRange(y, None), type_, None))  # noqa
            return cmp(dat_x, dat_y) if dat_x and dat_y else -1

        # Sort for date
        ret = sorted(ret_tasks + ret_obj, _datecomp)

        def _task_item_info(ref):
            ob = ref.to_object
            return {
                'title': ob.title,
                'url': ob.absolute_url(),
                'edit_url': addTokenToUrl(
                    ob.absolute_url() + '/@@edit'
                ),
                'state': plone.api.content.get_state(ob),
                'intid': ref.to_id
            }

        def _common_transitions(item):
            ret = []

            if IWFTask.providedBy(item):
                # Get the common transition for all referenced objects.
                task_items = getattr(item, 'task_items', [])
                transitions = []
                for ref in task_items:
                    ob = ref.to_object
                    _trans = [
                        (it['id'], it['name'])
                        for it in wftool.getTransitionsFor(ob)
                    ]
                    transitions.append(set(_trans))

                ret = None
                for transition in transitions:
                    if ret is None:
                        ret = transition
                        continue
                    ret = ret.intersection(transition)

                ret = list(ret) if ret else []

            else:
                # Get all current transitions for the given object
                transitions = None
                if type_ == 'effective':
                    transitions = EffectiveTransitionSource()
                else:
                    transitions = ExpiresTransitionSource(
                        transition=getattr(item, 'effective_transition', None),
                        portal_type=item.portal_type
                    )
                vocab = transitions(self.context)

                ret = [
                    (it.token, it.title)
                    for it in vocab
                ]

            return ret

        ret = [{
            'ob': it,
            'title': it.title,
            'url': it.absolute_url(),
            'delete_url': addTokenToUrl(
                it.absolute_url() + '/@@delete_confirmation'
            ),
            'edit_url': addTokenToUrl(
                it.absolute_url() + '/@@edit'
            ),
            'transition_date': getattr(it, 'task_date', getattr(it, type_, None)),  # noqa
            'transition': getattr(it, 'task_transition', getattr(it, type_ + '_transition', None)),  # noqa
            'state': plone.api.content.get_state(it),
            'uuid': IUUID(it),
            'is_task': IWFTask.providedBy(it),
            'task_items': [
                _task_item_info(ref)
                for ref in getattr(it, 'task_items', [])
            ],
            'common_transitions': _common_transitions(it)
        } for it in ret]

        return ret

    def items_effective(self):
        return self.items(type_='effective')

    def items_expires(self):
        return self.items(type_='expires')

    def __call__(self, *args, **kwargs):

        form = self.request.form
        uuid = form.get('uuid')

        infos = []
        warnings = []

        if uuid and form.get('run_task', None):
            wftype = form.get('wftype', None)
            task = uuidToObject(uuid)

            infos, warnings = run_task(
                task,
                include_wfer=True,
                wftype=wftype
            )

        elif uuid:

            items = [uuidToObject(uuid)]

            wftype = form.get('wftype', 'effective')

            if IWFTask.providedBy(items[0]):
                # Extend the list of items by all IWFEffectiveRange objects for
                # multi-editing those.
                items += [
                    it.to_object
                    for it in getattr(items[0], 'task_items', [])
                    if IWFEffectiveRange(it.to_object, None)
                ]

            transition_date = form.get('transition_date', None)
            transition = form.get('transition', None)
            ob_remove = form.get('ob_remove', None)

            for item in items:

                is_task = IWFTask.providedBy(item)

                if transition_date:
                    # Parse a Python datetime from a string using Zope DateTime
                    transition_date = DateTime(transition_date).asdatetime()
                    if is_task:
                        item.task_date = transition_date

                        infos.append(_(
                            'info_task_set_transition_date',
                            default=u'Set transition date ${transition_date} on task ${title}.',  # noqa
                            mapping={
                                'transition_date': transition_date,
                                'title': item.title
                            }
                        ))

                    else:
                        setattr(
                            IWFEffectiveRange(item),
                            wftype,
                            transition_date
                        )

                        infos.append(_(
                            'info_wf_set_transition_date',
                            default=u'Set ${wftype} transition date ${transition_date} on object ${title}.',  # noqa
                            mapping={
                                'wftype': wftype,
                                'transition_date': transition_date,
                                'title': item.title
                            }
                        ))

                if transition:
                    if is_task:
                        item.task_transition = transition

                        infos.append(_(
                            'info_task_set_transition',
                            default=u'Set transition ${transition} on task ${title}.',  # noqa
                            mapping={
                                'transition': transition,
                                'title': item.title
                            }
                        ))

                    else:
                        setattr(
                            IWFEffectiveRange(item),
                            wftype + '_transition',
                            transition
                        )

                        infos.append(_(
                            'info_wf_set_transition',
                            default=u'Set ${wftype} transition ${transition} on object ${title}.',  # noqa
                            mapping={
                                'wftype': wftype,
                                'transition': transition,
                                'title': item.title
                            }
                        ))

                if ob_remove and is_task:
                    # Remove the referenced item from the task
                    item.task_items = [
                        it for it in item.task_items
                        if it.to_id != int(ob_remove)
                    ]
                    intids = getUtility(IIntIds)
                    ob = intids.getObject(int(ob_remove))

                    infos.append(_(
                        'info_task_object_removed',
                        default=u'Removed referenced object ${obj_title} from task ${task_title}.',  # noqa
                        mapping={
                            'obj_title': ob.title,
                            'task_title': item.title
                        }
                    ))

                elif ob_remove == uuid:
                    # Clear the IWFEffectiveRange date and transition
                    setattr(
                        IWFEffectiveRange(item),
                        wftype,
                        None
                    )
                    setattr(
                        IWFEffectiveRange(item),
                        wftype + '_transition',
                        None
                    )

                    infos.append(_(
                        'info_wf_cleared',
                        default=u'Cleared the ${wftype} date and transition from ${title} and removed it from this list.',  # noqa
                        mapping={
                            'wftype': wftype,
                            'title': item.title
                        }
                    ))

                item.reindexObject()

        messages = IStatusMessage(self.request)
        for msg in infos:
            messages.add(msg, type=u"info")
        for msg in warnings:
            messages.add(msg, type=u"warning")

        return super(WFTaskOverviewView, self).__call__(*args, **kwargs)
