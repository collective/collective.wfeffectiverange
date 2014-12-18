
Changes
=======

1.6 (unreleased)
----------------

- Nothing changed yet.


1.5 (2014-12-18)
----------------

- added german translations
- js fix for existing expiration transition
- no caching/merging for ajax reload-vocab
  [agitator]


1.4 (2014-10-20)
----------------

- Bugfix: Subscriber had a problem with both transitions set.
  [jensens, 2014-10-20]


1.3 (2014-10-20)
----------------

- Bugfix: Marker interface on behavior was missing after a change so indexer
  did not grip. Due to a bug in plone.app.dexterity itself we cant procide
  the marker. So we bind the indexer to a general interface.
  [jensens, 2014-10-20]


1.2 (2014-10-18)
----------------

- Bugfix: Set a default to not fail if no transition was set initially.
  [jensens, 2014-10-18]

1.1 (2014-09-23)
----------------

- fix: keep transition after form validation error. respect base_url for view
  calls. fixes with vocab fetching.
  [benniboy, 2014-09-23]

1.0.1 (2014-09-22)
------------------

- fix: ticker view name was wrong.
  [jensens, 2014-09-22]

1.0 (2014-09-22)
----------------

- Initial implementation.
  [jensens, benniboy, 2014-09-22]
