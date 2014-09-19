
+ collective.wfpubex

+ self contained buildout mit 4.3 und dex

+ behavior mit allem drum und dran bauen. und mal die fields/fieldsets abschauen
  und nachbauen bzw erben is gscheida.

+ äh das datum von expiration muss größer sein als das pub date??
  mit invariant gelößt

+ von collective.wf autodoc und portal_workflow mal schauen wie man den workflow
  und die states mit transitions rausbekommt. alles in 1 vocab mtransitions
  weil dann später per js gecheckt wird: wenn pubtrans set dann
  dürfen bei exp trans nur transitions gewählt werden die dazu passen bzw nicht beißen

+ vocabulary bauen immer nur für aktuellencontext seinen jetzigen state,

+ die daten fürs vocabulary sollen vom punkt oben befüllt werden

+ im behavior a transition dropdown bauen mit daten vom vocab

+ validation bauen das wenn pub und oder exp date set, muss jeweils a transition
  selected sein

+ bei pubtrans nur transitions die aktuell möglich sind auf den state
+ bei exptrans

+ hm wenn pubtrans gesetzt dürfen bei exp trans nur die trans vom zukünftigen(pubtrans state)
  daherkommen

+ wenn pubtrans und exptrans, per js checken ob pub changed dann mit jsonview vocab für exp nachladen dürfen bei der exptrans
  wie gesagt nur transitions kommen die sich dann mit dem pubtrans bzw pubstate? nicht beißen

+ todo trans title durch trans shortname tauschen




TODO: if no workflow abfangen, und im behavior transitions ausschalten
todo wenn schon published dann republish möglich?? bzw felder ein ausblenden oder
a warning/infotext?

todo: testing






http://stackoverflow.com/questions/10947163/what-is-the-best-task-scheduling-approach-in-plone-4

+ zope chronjob anschauen und behavior mit dem chronjob verdrahten, so das
er die transition dann wirklich setzt. inkl gscheid gorillatesten :P

+ wenn cronjob ausgeführt dann auf das transition feld auf leer/erledigt default iwas waaaaaaaaaah setzen

- extra workflow automatisierte commentare

+ index bauen  für content der das field mal gesetzt hatte true /false

- before workflow subsriber hei darf ich der cronjobdude das ändern?
wenn pub oder exp transition gesetzt ist und irgnd eine workflow transition dann fehler
(redirect auf sich selber mit fehlermeldungstatusmessage error), auser die kommt vom cronjob


+ logging clockserver wenn schon clockserver läuft


- i18n strings in plone domain und messagestríngs baun

+ evtl ipubex dublincore machen?? fleißarbeit

behavior hübsch machen

