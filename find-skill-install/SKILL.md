---
name: find-skill
description: Search the skills.sh community registry and install a skill globally. Use this when the user wants to find, discover, or install a community skill — e.g. "find me a skill for X", "is there a skill that does Y?", "install a skill for Z", "search for a skill to help me with X". Always use this skill rather than building from scratch when the user wants to find existing community skills.
disable-model-invocation: true
allowed-tools: Bash
---

# Find & Install a Community Skill

Help the user discover and install a skill from the skills.sh community registry.

## Step 1: Ask what they need

Ask the user: "What kind of skill are you looking for?"

Wait for their answer, then use it as the search query.

## Step 2: Search the registry

Run this to get the top results from skills.sh:

```bash
npx --yes skills find "$QUERY" 2>&1 | sed 's/\x1b\[[0-9;]*m//g'
```

The results look like this (after stripping ANSI color codes):

```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@pr-review  1.2K installs
└ https://skills.sh/pr-review

some-repo@code-review  450 installs
└ https://skills.sh/code-review
```

Parse out up to 5 results. Each result gives you:
- `source` = the GitHub repo (e.g. `vercel-labs/agent-skills`)
- `name` = the skill name (e.g. `pr-review`)
- `installs` = formatted install count (e.g. `1.2K installs`)

## Step 3: Fetch descriptions from skills.sh

Each result includes a skills.sh URL (e.g. `https://skills.sh/pr-review`). Fetch descriptions from there — it's more reliable than guessing GitHub paths. Run all 5 in parallel:

```bash
for slug in "${SLUGS[@]}"; do
  curl -sf --max-time 5 "https://skills.sh/$slug" \
    | grep -o '<meta name="description" content="[^"]*"' \
    | sed 's/.*content="//;s/"//' \
    | cut -c1-150 \
    || echo ""
done &
wait
```

The slug comes from the skills.sh URL in the find output (e.g. `└ https://skills.sh/pr-review` → slug is `pr-review`).

If the fetch fails or returns empty (e.g. network issue), fall back silently to "No description available" for that entry — don't show an error.

## Step 4: Present the results

Show a clean numbered list (1 through 5):

```
Here are the top results for "code review":

1. pr-review  •  1.2K installs
   From: vercel-labs/agent-skills
   Reviews pull requests for issues, style, and best practices.

2. code-review  •  450 installs
   From: some-repo
   No description available.
```

If no results are found at all, tell the user and suggest they try different or simpler keywords.

## Step 5: Ask which to install

Ask: "Which one would you like to install? Enter a number (1–5), or say 'none' to cancel."

Wait for the user's answer.

## Step 6: Install the chosen skill

Run:

```bash
npx --yes skills add "$SOURCE@$SKILLNAME" -g -y 2>&1
```

Where `$SOURCE` and `$SKILLNAME` come from the chosen result.

On success, confirm: "✓ **$SKILLNAME** has been installed to your global skills folder (~/.claude/skills/). It's available across all your projects — you may need to restart Claude Code for it to appear."

If install fails, show the error and suggest: `npx skills add $SOURCE@$SKILLNAME -g`
