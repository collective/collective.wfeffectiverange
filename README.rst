=========================================
workflow based publication and expiration
=========================================


idea
====

Because the plone default publication and expiration functionality lacks in
terms of security we decided to write this addon.

For instance: If a contents publication date is not reached, it just does not
show up in the navigation, the search and so on.
But it can still be accessed directly,by a json request, or in many other ways.
The same for expired content.

For content needing more security, we want proper security using zopes access control
mechanism and CMF/plones workflow functionality.


usecases
========

usecase 1
---------

The user created an unpublished content.
The user sets a publication date and time in the future. With this date he has to select a valid
workflow transition.

valid means, it is a workflow transition which would be possible to select from plones default
plone workflow menu.

the selected transition will be automatically executed at the given date and time.


usecase 2
---------

First the user creates and publishes the content.
Then the user edits again and sets a expiration date and time in the future. With this date he has to select a valid workflow transition.

valid means, it is a workflow transition which would be possible to select from plones default
plone workflow menu.

the selected transition will be automatically executed at the given date and time.


usecase 3
---------

The user created an unpublished content.
Then the user sets a publication date and time in the future. With this date he has to select a valid
workflow transition.
valid means, it is a workflow transition which would be possible to select from plones default
plone workflow menu.

Then he also sets an expiration date and time in the future, after the publication date.
With this date he has to select a valid workflow transition.
Here valid means,a workflow transition from the target state of the transition entered for the publication associated states.

the selected transitions are automatically executed at the given date and time.


usecase 4
---------

The user has set an publication or expiration date like in the usecases 1, 2 or 3.
The user selects a workflow from the plone default workflow menu, or invokes it in any
other way. The workflow transition will be aborted and an error message is shown.


realization
===========

The usecases are implemented by providing a dexterity behavior, zope cronjob and
a workflow subscriber.

For each content type where this behavior is set, it will lookup the workflow
and get the possible transitions and provides them as a zope vocabulary.
It will also make checks so that that the selected transitions dont
interfer with each other.

Under the edit section, the dates tab will be replaced.
This behavior has the same fields as the usual publication behavior but adds two
more fields for transition selection, including vocabularies,validations
and invariants.

In order to provide a proper vocabulary for the expiration date after a publishing
date is set, a javascript and a serverside json view deliver the valid transitions.

zope cronjob insertusefulinfohere:P


limitations
===========

no support if a content type has two workflows
