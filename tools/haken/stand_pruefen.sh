#!/bin/sh
# Hook am Ende einer Antwort (Stop): erinnert einmal an Commit und Push (CLAUDE.md: Commit nach jedem
# Teilschritt, dann pushen). Läuft der Hook schon aus seiner eigenen Erinnerung heraus, bleibt er still.
#
# Von Hand:  echo '{}' | sh tools/haken/stand_pruefen.sh
eingabe=$(cat)
case "$eingabe" in *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) exit 0 ;; esac

cd "$(dirname "$0")/../.." || exit 0
offen=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
voraus=$(git rev-list --count '@{u}..HEAD' 2>/dev/null || echo 0)
[ "$offen" = 0 ] && [ "$voraus" = 0 ] && exit 0

grund="Git: $offen Dateien nicht committet, $voraus Commits nicht gepusht."
grund="$grund Ist der Teilschritt fertig, jetzt committen und pushen (CLAUDE.md)."
grund="$grund Ist er es nicht (z. B. Rückfrage an den Nutzer offen), das in einem Satz sagen und enden."
printf '{"decision":"block","reason":"%s"}\n' "$grund"
