---
name: repo-sync-check-v2
description: Aesop remote-state check via git fetch (clone-based)
---

Aesop repo sync check — verify origin/main has new commits since the last run and report them. Canonical local repo is C:\Users\scott\Code\Aesop but this task does NOT mount it — it clones fresh to /tmp each run.

Run this Bash block:

```
set -e
mkdir -p /tmp/aesop-check && cd /tmp/aesop-check
git config --global credential.helper store 2>/dev/null || true
echo "https://AesopScott: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@github.com" > ~/.git-credentials
git config --global user.email "ravenshroud@gmail.com"
git config --global user.name "Scott"
rm -rf /tmp/aesop-check/Aesop
git clone --depth 20 https://github.com/AesopScott/Aesop.git /tmp/aesop-check/Aesop
cd /tmp/aesop-check/Aesop
echo "=== Last 10 commits on main ==="
git log --oneline -10
echo "=== Commits in the last 35 minutes ==="
git log --oneline --since="35 minutes ago"
```

Summarize: how many commits in the last 35 minutes and what they changed. If none, say "no new commits" and stop. If the clone fails, report the error plainly and stop.