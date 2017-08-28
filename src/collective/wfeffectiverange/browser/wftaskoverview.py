# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.event.base import default_timezone
from plone.app.uuid.utils import uuidToObject
from plone.event.utils import pydt
from plone.protect.utils import addTokenToUrl
from plone.uuid.interfaces import IUUID
from zExceptions import Redirect
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from collective.wfeffectiverange.behaviors import IWFTask

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

        def _common_transitions(task_items):
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

            return list(ret) if ret else []

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
            'common_transitions': _common_transitions(
                getattr(it, 'task_items', [])
            )
        } for it in ret]

        return ret

    def items_effective(self):
        return self.items(type_='effective')

    def items_expired(self):
        return self.items(type_='expired')

    def __call__(self, *args, **kwargs):

        form = self.request.form
        task_uid = form.get('task_uid')

        if task_uid:
            task = uuidToObject(task_uid)

            task_date = form.get('task_date', None)
            if task_date:
                # First, parse a Python datetime from a time string.
                # For this, we let Zope DateTime do the parsing, but it might
                # return a wrong zone. DateTime.asdatetime returns a Python
                # datetime without timezone information.
                # We apply the default timezone via pydt then.
                # Cries for a utility method in plone.event or plone.app.event.
                task_date = pydt(
                    DateTime(task_date).asdatetime(),
                    default_timezone(self.context, as_tzinfo=True)
                )
                task.task_date = task_date

            task_transition = form.get('task_transition', None)
            if task_transition:
                task.task_transition = task_transition

            ob_remove = form.get('ob_remove', None)
            if ob_remove:
                task.task_items = [
                    it for it in task.task_items
                    if it.to_id != int(ob_remove)
                ]

            # Redirect to this view to exclude all url parameters, so that by
            # reloading the form isn't processed again.
            transaction.commit()
            raise Redirect(self.protected_view_url)

        return super(WFTaskOverviewView, self).__call__(*args, **kwargs)
