# -*- coding: utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile


def reload_profile(context):
    loadMigrationProfile(
        context,
        'profile-collective.wfeffectiverange:default'
    )
