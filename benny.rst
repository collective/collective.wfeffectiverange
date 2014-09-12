
collective.wfpubex

self contained buildout mit 4.3 und dex

behavior mit allem drum und dran bauen. und mal die fields/fieldsets abschauen
und nachbauen bzw erben is gscheida.

 evtl check das datums für pub und exp date nur in zukunft sein fürfen

äh das datum von expiration muss größer sein als das pub date??


von collective.wf autodoc und portal_workflow mal schauen wie man den workflow
und die states mit transitions rausbekommt. alles in 1 vocab mtransitions
weil dann später per js gecheckt wird: wenn pubtrans set dann
dürfen bei exp trans nur transitions gewählt werden die dazu passen bzw nicht beißen

vocabulary bauen immer nur für aktuellencontext seinen jetzigen state,
ala kupsite evtl mit sourcebinder:
transition1
transition2
..



die daten fürs vocabulary sollen vom punkt oben befüllt werden

im behavior a transition dropdown bauen mit daten vom vocab

validation bauen das wenn pub und oder exp date set, muss jeweils a transition
selected sein
test schreibn


so dann mehr validation und logic
bei pubtrans nur transitions die aktuell möglich sind auf den state
dito bei exptrans



wenn pubtrans und exptrans, per js checken ob pub changed dann mit jsonview vocab für exp nachladen dürfen bei der exptrans
wie gesagt nur transitions kommen die sich dann mit dem pubtrans bzw pubstate? nicht beißen
inlinevalidation test schreiben


nochmal genauer testen ob ok




zope chronjob anschauen und behavior mit dem chronjob verdrahten, so das
er die transition dann wirklich setzt. inkl gscheid gorillatesten :P
wenn cronjob ausgeführt dann auf das transition feld auf leer/erledigt default iwas waaaaaaaaaah setzen
extra workflow automatisierte commentare

index bauen  für content der das field mal gesetzt hatte true /false

before workflow subsriber hei darf ich der cronjobdude das ändern?
wenn pub oder exp transition gesetzt ist und irgnd eine workflow transition dann fehler
(redirect auf sich selber mit fehlermeldungstatusmessage error), auser die kommt vom cronjob



i18n strings in plone domain und messagestríngs baun


behavior hübsch machen












