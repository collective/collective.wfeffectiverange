#! /bin/sh

I18NDOMAIN="collective.wfeffectiverange"
PACKAGENAME="src/collective/wfeffectiverange"

# Synchronise the templates and scripts with the .pot.
# All on one line normally:
../../bin/i18ndude rebuild-pot --pot `pwd`/${PACKAGENAME}/locales/${I18NDOMAIN}.pot \
    --create ${I18NDOMAIN} --exclude "node_modules"\
   .

# Synchronise the resulting .pot with all .po files
for po in `pwd`/${PACKAGENAME}/locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    ../../bin/i18ndude sync --pot `pwd`/${PACKAGENAME}/locales/${I18NDOMAIN}.pot $po
done
