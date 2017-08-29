# -*- coding: utf-8 -*-
from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask
from DateTime import DateTime
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.dexterity.behaviors.metadata import IPublication
from plone.app.event.base import default_timezone
from plone.app.event.base import DT
from plone.app.uuid.utils import uuidToObject
from plone.event.utils import pydt
from plone.protect.utils import addTokenToUrl
from plone.uuid.interfaces import IUUID
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import plone.api
import transaction


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
        # Also, get the object as we need it anyways.
        ret_obj = [
            it.getObject()
            for it in ret_obj
            if intids.getId(it.getObject()) not in task_items_ids
        ]

        def _datecomp(x, y):
            dat_x = getattr(x, 'task_date', getattr(x, type_, None))
            dat_y = getattr(y, 'task_date', getattr(y, type_, None))
            return cmp(dat_x, dat_y)

        # Sort for date
        ret = sorted(ret_tasks + ret_obj, _datecomp)

        def _task_item_info(ref):
            ob = ref.to_object
            return {
                'title': ob.title,
                'url': ob.absolute_url(),
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
                ret = [
                    (it['id'], it['name'])
                    for it in wftool.getTransitionsFor(item)
                ]

            return ret

        ret = [{
            'ob': it,
            'title': it.title,
            'url': it.absolute_url(),
            'transition_date': getattr(it, 'task_date', getattr(it, type_, None)),  # noqa
            'transition': getattr(it, 'task_transition', getattr(it, type_ + '_transition', None)),  # noqa
            'state': plone.api.content.get_state(it),
            'uuid': IUUID(it),
            'is_wftask': IWFTask.providedBy(it),
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

        if uuid:

            items = [uuidToObject(uuid)]

            wftype = form.get('wftype', 'effective')

            if IWFTask.providedBy(items[0]):
                items += [
                    it.to_object for it in getattr(items[0], 'task_items', [])
                ]

            transition_date = form.get('transition_date', None)
            transition = form.get('transition', None)
            ob_remove = form.get('ob_remove', None)

            for item in items:

                is_task = IWFTask.providedBy(item)

                if transition_date:
                    # First, parse a Python datetime from a time string.  For
                    # this, we let Zope DateTime do the parsing, but it might
                    # return a wrong zone. DateTime.asdatetime returns a Python
                    # datetime without timezone information.
                    # We apply the default timezone via pydt then.
                    # Cries for a utility method in plone.event or p.a.event.
                    transition_date = pydt(
                        DateTime(transition_date).asdatetime(),
                        default_timezone(self.context, as_tzinfo=True)
                    )
                    if is_task:
                        item.task_date = transition_date
                    else:
                        setattr(
                            IPublication(item),
                            wftype,
                            DT(transition_date)
                        )

                if transition:
                    if is_task:
                        item.task_transition = transition
                    else:
                        setattr(
                            IWFEffectiveRange(item),
                            wftype + '_transition',
                            transition
                        )

                if ob_remove and is_task:
                    item.task_items = [
                        it for it in item.task_items
                        if it.to_id != int(ob_remove)
                    ]

                item.reindexObject()

            transaction.commit()
            return "Saved"

        return super(WFTaskOverviewView, self).__call__(*args, **kwargs)
