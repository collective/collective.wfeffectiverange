============================================================
Workflow transition based on publication and expiration date
============================================================

Once one of the effective range dates was reached an automatic workflow transition is executed and changes the workflow state with its managed permissions.

This is intended as an alternative implementation of the `Dexterity <http://docs.plone.org/external/plone.app.dexterity/docs/index.html>`_ IPublication behavior.

.. contents:: Table of Contents

Motivation
==========

Because the Plone default publication and expiration functionality lacks in terms of security we decided to create this addon.

For instance: In default Plone if a contents publication date is not reached, it does not show up in the navigation, the search and so on.
But it can still be accessed directly, by entering its URL, by a json request, or in many other ways. The same is true for expired content.

For contents that need more security, we want proper security handling using zopes access control mechanism and CMF/plones workflow functionality.

Installation
============

In your buildout or ``setup.py`` depend on ``collective.wfeffectiverange``.

Properly configure `Products.cron4plone as described here <https://pypi.python.org/pypi/Products.cron4plone/1.1.10>`_.

Run buildout.

In your profiles ``metadata.xml`` depend on ``profile-collective.wfeffectiverange:default`` or manually activate it in Plone control panels addon section.

In your content types GenericSetup XML file replace ``<element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>`` by::

  <element value="plone.app.dexterity.behaviors.metadata.IBasic"/>
  <element value="collective.wfeffectiverange.behaviors.IWFEffectiveRange"/>
  <element value="plone.app.dexterity.behaviors.metadata.ICategorization"/>
  <element value="plone.app.dexterity.behaviors.metadata.IOwnership"/>

Alternatively - when working TTW - do the same in the ``Dexterity content types`` control panel under the Behavior tab.

Configure the cronjob in the Plone control panel cron4plone section.
To check every minute enter::

    * * * * portal/@@wfeffectiverange-ticker


Use cases
=========

On Publish
----------

- The user creates an unpublished content item.
- The user sets a publication date and time in the future. With this date he has to select a valid workflow transition.
- Valid means, it is a workflow transition which would be possible to select from plones default plone workflow menu.
- The selected transition will be automatically executed at the given date and time.


On Expiration
-------------

- First the user creates and publishes the content.
- Then the user edits again and sets a expiration date and time in the future. With this date he has to select a valid workflow transition.
- Valid means, it is a workflow transition which would be possible to select from plones default plone workflow menu.
- The selected transition will be automatically executed at the given date and time.


On Both
-------

- The user created an unpublished content.
- Then the user sets a publication date and time in the future. With this date he has to select a valid workflow transition.
- Valid means, it is a workflow transition which would be possible to select from plones default plone workflow menu.
- Then he also sets an expiration date and time in the future, after the publication date.
- With this date he has to select a valid workflow transition.
- Here valid means, a workflow transition from the target state of the transition entered for the publication associated states.
- The selected transitions are automatically executed at the given date and time.


Abort manual set transition
---------------------------

- The user has set an publication or expiration date like in the use case 1, 2 or 3.
- The user selects a workflow from the plone default workflow menu, or invokes it in any other way.
- The workflow transition will be aborted and an error message is shown.


Publication date in past
------------------------

- The user edits content created by use case 1 after the publication date and the transition was executed.
- Now the publication transition field is empty and can not be set because the publication date is in the past.


Re-Editing
----------

- The user edits content created by use case 1 after the publication date and the transition was executed.
- Then the user can follow use case 2.


Implementation
==============

The use cases are implemented by providing a dexterity behavior, zope cronjob (cron4plone) and a workflow subscriber.

For each content type where this behavior is set, it will lookup the workflow gets the possible transitions and provides them as a zope vocabulary. It will also check that the selected transitions don't interfere with each other.

Under the edit section, the dates tab will be replaced.
This behavior will replace publication/expiration fields within the dates tab and adds a fields to select the target workflow transition, including vocabularies, validations and invariants.

A server-side json view delivers the transitions for the expiration date after a publishing date is set, in order to provide a proper vocabulary.

In order to make it work, you have to configure a cron job to check if the desired workflow transition date has been met. See install section


Limitations
===========

No support if a content type has two workflows.


Source Code and Contributions
=============================

If you want to help with the development (reporting, improvement, update, bug-fixing, ...) of ``collective.wfeffectiverange`` this is a great idea!

Please file any issues or ideas for enhancement at the `issue tracker <https://github.com/collective/collective.wfeffectiverange/issues>`_.

The code is located in the `github collective <https://github.com/collective/collective.wfeffectiverange>`_.

You can clone it or `get access to the github-collective <http://collective.github.com/>`_ and work directly on the project.

Maintainer is Jens Klein and the BlueDynamics Alliance developer team. We appreciate any contribution and if a release is needed to be done on pypi,
please just contact one of us `dev@bluedynamics dot com <mailto:dev@bluedynamics.com>`_

Contributors
============

- Benjamin Stefaner <bs@kleinundpartner.at> - development

- Jens W. Klein <jens@bluedynamics.com> - development

- Peter Holzer <peter.holzer@agitator.com> - use case, development

