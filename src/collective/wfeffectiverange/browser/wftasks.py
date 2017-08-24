# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.folder import FolderView

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
        ret = [ref.to_object for ref in refs if ref]
        return ret

    def task_objects_info(self, task):
        objects = self.task_objects(task)
        wftool = plone.api.portal.get_tool('portal_workflow')

        ret = []
        for ob in objects:
            ret.append({
                'title': ob.title,
                'url': ob.absolute_url(),
                'workflows': u', '.join([wf.title for wf in wftool.getWorkflowsFor(ob)]),  # noqa
                'state': plone.api.content.get_state(ob)
            })

        return ret

    def common_transitions(self, task):
        wftool = plone.api.portal.get_tool('portal_workflow')
        transitions = []
        for ob in self.task_objects(task):
            ob_transitions = []
            wfs = wftool.getWorkflowsFor(ob)
            for wf in wfs:
                for state in wf.states.objectValues():
                    ob_transitions += list(state.getTransitions())
            transitions.append(set(ob_transitions))

        import pdb
        pdb.set_trace()

        ret = None
        for transition in transitions:
            if ret is None:
                ret = transition
                continue
            ret = ret.intersection(transition)

        return list(ret)
