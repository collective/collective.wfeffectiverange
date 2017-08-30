# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations


WFTASK_LOGGER_KEY = 'wftasklogger'


class WFTaskLogView(BrowserView):

    @property
    def log(self):
        import pdb
        pdb.set_trace()
        annotations = IAnnotations(self.context)
        tasklogger = annotations[WFTASK_LOGGER_KEY] or {}
        ret = sorted(
            tasklogger.items(),
            lambda x, y: cmp(DateTime(x), DateTime(y))
        )
        return ret
