# -*- coding: utf-8 -*-
from collective.wfscheduler import _
from collective.wfscheduler.behaviors import refs_to_objs
from plone.app.contenttypes.browser.folder import FolderView
from Products.CMFPlone.utils import safe_callable

import plone.api


class WFTasksOverviewView(FolderView):


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

    def task_objects(self, task):
        refs = getattr(task, 'task_items', [])
        for ref in refs:
            ref = ref.to_object
            if not ref:
                # Invalid
                return refs
