# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations


WFTASK_LOGGER_KEY = 'wftasklogger'


class WFTaskLogView(BrowserView):

    def log(self):
        annotations = IAnnotations(self.context)
        tasklogger = annotations.get(WFTASK_LOGGER_KEY, {})
        ret = sorted(
            tasklogger.items(),
            cmp=lambda x, y: cmp(DateTime(x[0]), DateTime(y[0])),
            reverse=True
        )
        return ret
