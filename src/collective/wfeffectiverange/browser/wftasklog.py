# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from operator import itemgetter


WFTASK_LOGGER_KEY = 'wftasklogger'


class WFTaskLogView(BrowserView):

    def log(self):
        annotations = IAnnotations(self.context)
        tasklogger = annotations.get(WFTASK_LOGGER_KEY, {})
        if tasklogger:
            print(tasklogger.items())
            ret = sorted(
                tasklogger.items(), key=itemgetter(0),
                reverse=True
            )
            return ret
