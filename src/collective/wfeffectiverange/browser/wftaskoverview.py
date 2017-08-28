# -*- coding: utf-8 -*-
# from collective.wfeffectiverange.behaviors import IWFEffectiveRange
from collective.wfeffectiverange.behaviors import IWFTask
from DateTime import DateTime
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.event.base import default_timezone
from plone.app.uuid.utils import uuidToObject
from plone.event.utils import pydt
from plone.protect.utils import addTokenToUrl
from plone.uuid.interfaces import IUUID
from zExceptions import Redirect

import plone.api
import transaction


class WFTaskOverviewView(FolderView):

    @property
    def protected_view_url(self):
        url = addTokenToUrl(self.context.absolute_url() + '/@@wftaskoverview')
        return url

    def tasks(self):
        ret = plone.api.content.find(**{
            'object_provides': IWFTask.__identifier__
        })
        return ret

    def wfeffectiverange_objs(self):
        ret_effective = plone.api.content.find(**{
            # 'object_provides': IWFEffectiveRange.__identifier__,
            'has_effective_transition': True
        })
        ret_expires = plone.api.content.find(**{
            # 'object_provides': IWFEffectiveRange.__identifier__,
            'has_expires_transition': True
        })
        ret = list(set(
            [it.getObject() for it in ret_effective] +
            [it.getObject() for it in ret_expires]
        ))

        def _publicationcomp(x, y):
            dat_x = x.effective or x.expires
            dat_y = y.effective or y.expires
            return cmp(dat_x, dat_y)

        ret = sorted(ret, _publicationcomp)
        ret = [{
            'title': it.title,
            'url': it.absolute_url(),
            'effective': getattr(it, 'effective', None),
            'effective_transition': getattr(it, 'effective_transition', None),
            'expires': getattr(it, 'expires', None),
            'expires_transition': getattr(it, 'expires_transition', None),
            'state': plone.api.content.get_state(it),
            'uuid': IUUID(it),
        } for it in ret]

        return ret

    def task_info(self, task):
        return {
            'title': task.title,
            'url': task.absolute_url(),
            'date': getattr(task, 'task_date', None),
            'transition': getattr(task, 'task_transition', None),
            'uuid': IUUID(task),
            'type': task.Type
        }

    def task_objects(self, task):
        refs = getattr(task, 'task_items', [])
        ret = [ref.to_object for ref in refs if ref]
        return ret

    def task_objects_info(self, task):
        wftool = plone.api.portal.get_tool('portal_workflow')

        ret = []
        refs = getattr(task, 'task_items', [])
        for ref in refs:
            ob = ref.to_object
            ret.append({
                'title': ob.title,
                'url': ob.absolute_url(),
                'workflows': u', '.join([wf.title for wf in wftool.getWorkflowsFor(ob)]),  # noqa
                'state': plone.api.content.get_state(ob),
                'intid': ref.to_id
            })

        return ret

    def common_transitions(self, task):
        wftool = plone.api.portal.get_tool('portal_workflow')
        transitions = []
        for ob in self.task_objects(task):
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
