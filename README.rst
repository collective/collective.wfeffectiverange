============================================================
Workflow transition based on publication and expiration date
============================================================

This is intended as an alternative implemention of the dexterity IPublication behavior.


Background
==========

Because the Plone default publication and expiration functionality lacks in terms of security we decided to write this addon.

For instance: If a contents publication date is not reached, it does not show up in the navigation, the search and so on.
But it can still be accessed directly, by a json request, or in many other ways. The same is true for expired content.

For contents that need more security, we want proper security handling using zopes access control mechanism and CMF/plones workflow functionality.


Usecases
========

Usecase 1
---------

- The user creates an unpublished content item.
- The user sets a publication date and time in the future. With this date he has to select a valid workflow transition.
- Valid means, it is a workflow transition which would be possible to select from plones default plone workflow menu.
- The selected transition will be automatically executed at the given date and time.


Usecase 2
---------

- First the user creates and publishes the content.
- Then the user edits again and sets a expiration date and time in the future. With this date he has to select a valid workflow transition.
- Valid means, it is a workflow transition which would be possible to select from plones default plone workflow menu.
- The selected transition will be automatically executed at the given date and time.


Usecase 3
---------

- The user created an unpublished content.
- Then the user sets a publication date and time in the future. With this date he has to select a valid workflow transition.
- Valid means, it is a workflow transition which would be possible to select from plones default plone workflow menu.
- Then he also sets an expiration date and time in the future, after the publication date.
- With this date he has to select a valid workflow transition.
- Here valid means, a workflow transition from the target state of the transition entered for the publication associated states.
- The selected transitions are automatically executed at the given date and time.


Usecase 4
---------

- The user has set an publication or expiration date like in the usecase 1, 2 or 3.
- The user selects a workflow from the plone default workflow menu, or invokes it in any other way. 
- The workflow transition will be aborted and an error message is shown.


Usecase 5
---------

- The user edits content created by usecase 1 after the publication date and the transition was executed.
- Now the publication transition field is empty and can not be set because the publication date is in the past.


Usecase 6
---------
- The user edits content created by usecase 1 after the publication date and the transition was executed.
- Then the user can follow usecase 2.


Implementation
==============

The usecases are implemented by providing a dexterity behavior, zope cronjob and a workflow subscriber.

For each content type where this behavior is set, it will lookup the workflow gets the possible transitions and provides them as a zope vocabulary. It will also check that the selected transitions dont interfer with each other.

Under the edit section, the dates tab will be replaced.
This behavior will replace publication/expiration fields within the dates tab and adds a fields to select the target workflow transition, including vocabularies, validations and invariants.

A serverside json view delivers the transitions for the expiration date after a publishing date is set, in order to provide a proper vocabulary.

In order to make it work, you have to configure a cron job to check if the desired workflow transition date has been met.


limitations
===========

no support if a content type has two workflows
