#!/usr/bin/env bash
# Rebuild every language variant of a translatable page from its canonical English source
# and the per-language JSON catalogs in /i18n.
#
# Usage:
#   scripts/i18n_build_all.sh                            # rebuilds courses.html for all 12 langs
#   scripts/i18n_build_all.sh ai-academy/courses.html    # explicit source path
#
# Languages are read from LANGS below. Add or remove codes here as Mod Gen evolves.
set -euo pipefail

LANGS=(es fr de hi ur zh fa ru ko ja ar sw)
SRC="${1:-ai-academy/courses.html}"
REL="${SRC#ai-academy/}"   # e.g. "courses.html"

# Output convention: ai-academy/modules/{lang}/<relpath>
# Keeps language folders out of the repo root.
for lang in "${LANGS[@]}"; do
  DST="ai-academy/modules/${lang}/${REL}"
  mkdir -p "$(dirname "$DST")"
  python3 scripts/i18n_build.py "$lang" "$SRC" "$DST"
done
