#!/bin/bash
# Doppelklick: schiebt alles, was hier fertig ist, auf GitHub.
# Liegt absichtlich im Projekt, damit niemand den Pfad suchen muss.
cd "$(dirname "$0")" || exit 1
echo "EKG-Spiel → GitHub"
echo
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "Stand vom $(date '+%d.%m.%Y %H:%M')"
  echo "  neue Änderungen eingepackt"
fi
VOR=$(git rev-list --count HEAD)
git push && echo && echo "fertig — $VOR Commits sind jetzt auf GitHub." \
         || { echo; echo "Push fehlgeschlagen. Meist fehlt die Anmeldung —"; \
              echo "einmal 'git push' hier im Terminal laufen lassen und Token eingeben."; }
echo
read -n 1 -s -r -p "Taste drücken zum Schließen."
