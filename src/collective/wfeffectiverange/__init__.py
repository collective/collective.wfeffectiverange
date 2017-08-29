# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('collective.wfeffectiverange')


# Permissions
security = ModuleSecurityInfo('collective.wfeffectiverange')

security.declarePublic('collective.wfeffectiverange.addTaskFolder')
setDefaultRoles('collective.wfeffectiverange: Add Task Folder', ('Manager', 'Site Administrator'))  # noqa

security.declarePublic('collective.wfeffectiverange.addTask')
setDefaultRoles('collective.wfeffectiverange: Add Task', ('Manager', 'Site Administrator', 'Reviewer'))  # noqa
