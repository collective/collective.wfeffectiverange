class WFTasksOverviewView(BrowserView):

    def __init__(self, context, request):
        pass

# -*- coding: utf-8 -*-
from collective.wfscheduler import _
from collective.wfscheduler.behaviors import refs_to_objs
from plone.app.contenttypes.browser.folder import FolderView
from Products.CMFPlone.utils import safe_callable

import plone.api


class WFTaskOverviewView(FolderView):

    def results(self, **kwargs):
        # Default is to show all.
        kwargs['portal_type'] = 'WFTask'
        filter_ = self.request.form.get('filter')
        if filter_ == 'active':
            kwargs['is_active'] = True
        elif filter_ == 'inactive':
            kwargs['is_active'] = False
        return super(WFTaskFolderView, self).results(**kwargs)

    @property
    def filter_selected(self):
        filter_ = self.request.form.get('filter')
        return {
            'active': ' selected' if filter_ == 'active' else '',
            'inactive': ' selected' if filter_ == 'inactive' else '',
            'all': ' selected' if filter_ not in ('active', 'inactive') else ''
        }

    @property
    def tabular_fields(self):

        return [
            {'title': _('label_title', default=u"Title"), 'name': 'title'},
            {'title': _('label_task_items', default=u'Task items'), 'name': 'task_items'},  # noqa
            {'title': _('label_task_transition', default=u'Task action'), 'name': 'task_transition'},  # noqa
            {'title': _('label_task_date', default=u'Task task date'), 'name': 'task_date'},  # noqa
            {'title': _('label_task_active', default=u'Active?'), 'name': 'task_active'},  # noqa
        ]

    def tabular_fielddata(self, item, fieldname):
        value = getattr(item, fieldname, '')
        if safe_callable(value):
            value = value()

        if fieldname == 'task_date' and value:
            value = self.toLocalizedTime(value, long_format=1)

        if fieldname == 'task_items':

            value = u'\n'.join([
                u'<li><a class="pat-plone-modal" href="{1}">{0} ({2})</a></li>'.format(  # noqa
                    it.Title(),
                    it.absolute_url(),
                    plone.api.content.get_state(it)
                ) for it in refs_to_objs(value)
            ])

            value = u'<ul>\n{0}\n</ul>'.format(value)

        return {
            # 'title': _(fieldname, default=fieldname),
            'value': value
        }

