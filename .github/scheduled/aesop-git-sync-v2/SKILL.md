---
name: aesop-git-sync-v2
description: Aesop repo health check (clone-based). Canonical local path: C:\Users\scott\Code\Aesop
---

Aesop git sync — passive health check for https://github.com/AesopScott/Aesop.git. The canonical local working repo is C:\Users\scott\Code\Aesop; Scott pushes manually from there via GitHub Desktop. This task does NOT push and does NOT mount the local repo — it clones fresh to /tmp each run and reports remote state.

Run this single Bash block and report its output:

```
set -e
mkdir -p /tmp/aesop-sync && cd /tmp/aesop-sync
git config --global credential.helper store
echo "https://AesopScott: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@github.com" > ~/.git-credentials
git config --global user.email "ravenshroud@gmail.com"
git config --global user.name "Scott"
rm -rf /tmp/aesop-sync/Aesop
git clone --depth 5 https://github.com/AesopScott/Aesop.git /tmp/aesop-sync/Aesop
cd /tmp/aesop-sync/Aesop
echo "=== Last 5 commits on main ==="
git log --oneline -5
echo "=== HEAD details ==="
git log -1 --format="%H%n%an <%ae>%n%ad%n%s" --date=iso
git fetch origin eval-system 2>/dev/null && echo "eval-system branch reachable" || echo "eval-system branch not found"
```

If the clone fails (DNS/network in the sandbox), report the error plainly and stop — do NOT retry in a loop. Do not attempt to mount the local repo.