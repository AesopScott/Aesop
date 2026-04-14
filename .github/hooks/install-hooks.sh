#!/bin/sh
# ──────────────────────────────────────────────────────────
# Install git hooks from .github/hooks/ into .git/hooks/
# Run once after cloning:  sh .github/hooks/install-hooks.sh
# ──────────────────────────────────────────────────────────

HOOK_SRC="$(git rev-parse --show-toplevel)/.github/hooks"
HOOK_DST="$(git rev-parse --show-toplevel)/.git/hooks"

if [ ! -d "$HOOK_SRC" ]; then
  echo "Error: $HOOK_SRC not found. Are you in the repo root?"
  exit 1
fi

INSTALLED=0
for HOOK in "$HOOK_SRC"/*; do
  NAME=$(basename "$HOOK")

  # Skip this installer script
  [ "$NAME" = "install-hooks.sh" ] && continue

  cp "$HOOK" "$HOOK_DST/$NAME"
  chmod +x "$HOOK_DST/$NAME"
  echo "  Installed: $NAME"
  INSTALLED=$((INSTALLED + 1))
done

echo ""
echo "Done — $INSTALLED hook(s) installed to .git/hooks/"
