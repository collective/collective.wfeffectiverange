# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.uuid.utils import uuidToObject
from plone.protect.utils import addTokenToUrl
from plone.uuid.interfaces import IUUID
from zExceptions import Redirect

import plone.api


class WFTasksOverviewView(FolderView):

    def protected_view_url(self):
        url = addTokenToUrl(self.context.absolute_url() + '/@@workflow-tasks')
        return url

    def tasks_effective(self):
        ret = plone.api.content.find(**{
            'portal_type': 'WFTaskEffective'
        })
        return ret

    def tasks_expired(self):
        ret = plone.api.content.find(**{
            'portal_type': 'WFTaskExpired'
        })
        return ret

    def task_info(self, task):
        return {
            'title': task.title,
            'url': task.absolute_url(),
            'date': task.task_date,
            'transition': task.task_transition,
            'uuid': IUUID(task)
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

        return list(ret)

    def __call__(self, *args, **kwargs):

        form = self.request.form
        task_uid = form.get('task_uid')

        if task_uid:
            task = uuidToObject(task_uid)

            task_date = form.get('task_date', None)
            if task_date is not None:
                task.task_date = task_date

            task_transition = form.get('task_transition', None)
            if task_transition is not None:
                task.task_transition = task_transition

            ob_remove = form.get('ob_remove', None)
            if ob_remove:
                task.task_items = [
                    it for it in task.task_items
                    if it.to_id != int(ob_remove)
                ]

        return super(WFTasksOverviewView, self).__call__(*args, **kwargs)
