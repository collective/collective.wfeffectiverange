# -*- coding: utf-8 -*-
from collective.wfeffectiverange import _
from collective.wfeffectiverange import utils
from collective.wfeffectiverange.browser.wfticker import run_task
from collective.wfeffectiverange.vocabulary import EffectiveTransitionSource
from collective.wfeffectiverange.vocabulary import ExpiresTransitionSource
from DateTime import DateTime
from plone.app.contenttypes.browser.folder import FolderView
from plone.app.uuid.utils import uuidToObject
from plone.app.widgets.utils import get_datetime_options
from plone.protect.utils import addTokenToUrl
from plone.uuid.interfaces import IUUID
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from pprint import pprint

import json
import plone.api


class WFTaskOverviewView(FolderView):

    @property
    def protected_view_url(self):
        url = addTokenToUrl(self.context.absolute_url() + '/@@wftaskoverview')
        return url

    @property
    def pickadate_options(self):
        return json.dumps(get_datetime_options(self.request))

    def items(self, type_):
        intids = getUtility(IIntIds)
        wftool = plone.api.portal.get_tool('portal_workflow')

        query = {'portal_type': 'WFTask' + type_.capitalize()}
        ret_tasks = plone.api.content.find(**query)
        ret_tasks = [it.getObject() for it in ret_tasks]

        # Get all task_items ids for IWFEffectiveRange object filtering.
        task_items_ids = []
        for task in ret_tasks:
            task_items_ids += [it.to_id for it in task.task_items]

        query = {'has_' + type_ + '_transition': True}
        ret_obj = plone.api.content.find(**query)

        # Filter all IWFEffectiveRange objects, which are already related in an
        # IWFTask object.
        # Also, get the object as we need it anyways.
        ret_obj = [it.getObject() for it in ret_obj]
        ret_obj = [
            it
            for it in ret_obj
            if utils.is_wfeffectiverange(it)
            and intids.getId(it) not in task_items_ids
        ]

        # def _datecomp(x, y):
        #     dat_x = getattr(x, 'task_date', utils.get_pub_date(x, type_))
        #     dat_y = getattr(y, 'task_date', utils.get_pub_date(y, type_))
        #     _cmp = cmp(dat_x, dat_y) if dat_x and dat_y else -1
        #     return _cmp

        def _dategetter(x):
            return getattr(x, 'task_date', utils.get_pub_date(x, type_))

        # Sort for date
        ret = sorted(ret_tasks + ret_obj, key=_dategetter)

        def _task_item_info(ref, type_):
            ob = ref.to_object
            return {
                'title': ob.title,
                'url': ob.absolute_url(),
                'edit_url': addTokenToUrl(
                    ob.absolute_url() + '/@@edit'
                ),
                'state': plone.api.content.get_state(ob),
                'intid': ref.to_id,
                'transition_date': utils.get_pub_date(ob, type_),
                'transition': getattr(
                    ob,
                    type_ + '_transition',
                    None
                ) or _('label_no_transition', 'No transition'),
                'is_task': utils.is_task(ob),
                'is_wfeff': utils.is_wfeffectiverange(ob),
            }

        def _common_transitions(item):
            ret = []

            if utils.is_task(item):
                # Get the common transition for all referenced objects.
                task_items = getattr(item, 'task_items', [])
                transitions = []
                for ref in task_items:
                    ob = ref.to_object
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

                ret = list(ret) if ret else []

            else:
                # Get all current transitions for the given object
                transitions = None
                if type_ == 'effective':
                    transitions = EffectiveTransitionSource()
                else:
                    transitions = ExpiresTransitionSource()
                vocab = transitions(item)

                ret = [
                    (it.token, it.title)
                    for it in vocab
                ]

            return ret

        ret = [{
            'ob': it,
            'title': it.title,
            'url': it.absolute_url(),
            'delete_url': addTokenToUrl(
                it.absolute_url() + '/@@delete_confirmation'
            ),
            'edit_url': addTokenToUrl(
                it.absolute_url() + '/@@edit'
            ),
            'transition_date': getattr(it, 'task_date', None)
                if utils.is_task(it)
                else utils.get_pub_date(it, type_),
            'transition': (getattr(it, 'task_transition', None)
                if utils.is_task(it)
                else getattr(it, type_ + '_transition', None)
            ) or _('label_no_transition', 'No transition'),
            'state': plone.api.content.get_state(it),
            'uuid': IUUID(it),
            'is_task': utils.is_task(it),
            'is_wfeff': utils.is_wfeffectiverange(it),
            'task_items': [
                _task_item_info(ref, type_)
                for ref in getattr(it, 'task_items', [])
            ],
            'common_transitions': _common_transitions(it)
        } for it in ret]

        return ret

    def items_effective(self):
        return self.items(type_='effective')

    def items_expires(self):
        return self.items(type_='expires')

    def __call__(self, *args, **kwargs):

        form = self.request.form
        uuid = form.get('uuid', None)
        wftype = form.get('wftype', None)

        infos = []
        warnings = []

        if uuid and wftype and form.get('run_task', None):
            task = uuidToObject(uuid)

            infos, warnings = run_task(
                task,
                include_wfer=True,
                wftype=wftype
            )

        elif uuid:

            items = [uuidToObject(uuid)]

            if utils.is_task(items[0]):
                # Extend the list of items by all IWFEffectiveRange objects for
                # multi-editing those.
                items += [
                    it.to_object
                    for it in getattr(items[0], 'task_items', [])
                    if utils.is_wfeffectiverange(it.to_object)
                ]

            transition_date = form.get('transition_date', None)
            transition = form.get('transition', None)
            ob_remove = form.get('ob_remove', None)

            for item in items:

                is_task = utils.is_task(item)
                is_wfeffectiverange = utils.is_wfeffectiverange(item)

                item_url = item.absolute_url()

                if transition_date is not None:
                    # Parse a Python datetime from a string using Zope DateTime
                    # If set, but empty clear the field with None.
                    transition_date = DateTime(transition_date).asdatetime() if transition_date else None  # noqa
                    if is_task:
                        item.task_date = transition_date

                        infos.append(_(
                            'info_task_set_transition_date',
                            default=u'Set transition date ${transition_date} on task ${url}.',  # noqa
                            mapping={
                                'transition_date': transition_date,
                                'url': item_url
                            }
                        ))

                    elif is_wfeffectiverange and wftype:
                        utils.set_pub_date(item, wftype, transition_date)
                        infos.append(_(
                            'info_wf_set_transition_date',
                            default=u'Set ${wftype} transition date ${transition_date} on object ${url}.',  # noqa
                            mapping={
                                'wftype': wftype,
                                'transition_date': transition_date,
                                'url': item_url
                            }
                        ))

                if transition is not None:
                    if is_task:
                        item.task_transition = transition

                        infos.append(_(
                            'info_task_set_transition',
                            default=u'Set transition "${transition}" on task ${url}.',  # noqa
                            mapping={
                                'transition': transition,
                                'url': item_url
                            }
                        ))

                    elif is_wfeffectiverange and wftype:
                        setattr(
                            item,
                            wftype + '_transition',
                            transition
                        )

                        infos.append(_(
                            'info_wf_set_transition',
                            default=u'Set ${wftype} transition "${transition}" on object ${url}.',  # noqa
                            mapping={
                                'wftype': wftype,
                                'transition': transition,
                                'url': item_url
                            }
                        ))

                if is_task and ob_remove:
                    # Remove the referenced item from the task
                    item.task_items = [
                        it for it in item.task_items
                        if it.to_id != int(ob_remove)
                    ]
                    intids = getUtility(IIntIds)
                    ob = intids.getObject(int(ob_remove))

                    infos.append(_(
                        'info_task_object_removed',
                        default=u'Removed referenced object ${obj_url} from task "${task_title}".',  # noqa
                        mapping={
                            'ob_url': ob.absolute_url(),
                            'task_title': item.title
                        }
                    ))

                elif is_wfeffectiverange and ob_remove == uuid and wftype:
                    # Clear the IWFEffectiveRange date and transition
                    utils.set_pub_date(item, wftype, None)
                    setattr(item, wftype + '_transition', None)

                    infos.append(_(
                        'info_wf_cleared',
                        default=u'Cleared the ${wftype} date and transition from ${url} and removed it from this list.',  # noqa
                        mapping={
                            'wftype': wftype,
                            'url': item_url
                        }
                    ))

                item.reindexObject()

        messages = IStatusMessage(self.request)
        for msg in infos:
            messages.add(msg, type=u"info")
        for msg in warnings:
            messages.add(msg, type=u"warning")

        return super(WFTaskOverviewView, self).__call__(*args, **kwargs)
