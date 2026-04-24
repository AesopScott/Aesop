# Course Drift Report

**Source of truth for this report:** course folders with `<slug>-m1.html`
under `ai-academy/modules/` in the **local working copy of this repo**.
This is not necessarily the same as:

- **GitHub `origin/main`** — usually identical if this worktree is synced, but
  could differ if commits are pending push or if `main` advanced during this run.
- **Production web server (aesopacademy.org)** — reflects whatever was last
  deployed; may lag behind or differ from GitHub `main` depending on deploy state.

This script is read-only — nothing was modified.

- Disk (truth): **63** courses
- Registry live: **50** courses  (50 with a URL)
- courses.html `--live` buttons: **66**  (total mega-links: 100)
- courses.html panels (unique `dv-N` ids): **30**  (with `core-badge-live`: 73)
- dashboard.html COURSES array: **65** entries
- stats.json coursesLive: **54**

## Registry vs Disk

**14 on disk, missing from registry:**
- `ai-and-climate`
- `ai-and-fake-information`
- `ai-bias-and-fairness`
- `ai-for-small-business-managers`
- `building-agents-vertex-ai`
- `coded-unfair-ai-bias-exposed`
- `creating-with-ai-tools`
- `how-large-language-models-work`
- `make-it-yours-creating-with-ai`
- `the-alignment-problem`
- `the-context-window-race`
- `the-future-of-intelligence`
- `vertex-ai-data-agents`
- `whats-really-inside-ai`

**1 in registry, no folder on disk:**
- `how_large_language_models_work`

**0 in registry but not marked `live` (though folder exists):**
- _(none)_

**83 registry entries with no URL (unusable for matching):**
- key=`aip-ai-accessibility`  title='AI for Accessibility'  status=coming-soon
- key=`aip-ai-alignment-for-everyone`  title='Teaching AI to Want Good Things'  status=coming-soon
- key=`aip-ai-and-your-creative-work`  title='AI as Your Creative Partner'  status=coming-soon
- key=`aip-ai-bias-and-fairness`  title='Understanding AI Bias and Fairness'  status=coming-soon
- key=`aip-ai-creativity-arts`  title='AI in Creativity and Arts'  status=coming-soon
- key=`aip-ai-data-literacy`  title='Data Literacy for AI'  status=coming-soon
- key=`aip-ai-decision-making`  title='AI in Decision Making'  status=coming-soon
- key=`aip-ai-ethics-everyday-choices`  title='Is This AI Fair to You?'  status=coming-soon
- key=`aip-ai-ethics-foundations`  title='AI Ethics: Right and Wrong'  status=coming-soon
- key=`aip-ai-for-job-hunting`  title='Get Hired Using AI'  status=coming-soon
- key=`aip-ai-for-small-business-owners`  title='AI Tools Every Small Business Needs'  status=coming-soon
- key=`aip-ai-governance-regulation`  title='AI Governance and Regulation'  status=coming-soon
- key=`aip-ai-in-journalism-and-media`  title='AI Reshaping News and Storytelling'  status=coming-soon
- key=`aip-ai-in-medicine-explained`  title='How AI Is Changing Healthcare'  status=coming-soon
- key=`aip-ai-misinformation`  title='AI and Misinformation'  status=coming-soon
- key=`aip-ai-music-and-audio-generation`  title='AI That Composes and Creates Sound'  status=coming-soon
- key=`aip-ai-privacy-and-security`  title='AI Privacy and Data Security'  status=coming-soon
- key=`aip-ai-safety-and-alignment`  title='Teaching AI to Do Good'  status=coming-soon
- key=`aip-ai-safety-and-alignment-basics`  title='Keeping AI Safe for Everyone'  status=coming-soon
- key=`aip-ai-safety-for-everyone`  title='Keeping AI Under Control'  status=coming-soon
- key=`aip-ai-side-hustle-money`  title='Make Real Money With AI'  status=coming-soon
- key=`aip-ai-tools-for-college`  title='AI That Actually Helps You Study'  status=coming-soon
- key=`aip-ai-tools-for-small-business`  title='AI Superpowers for Small Business'  status=coming-soon
- key=`aip-ai-work-and-automation-deep-dive`  title='AI, Automation, and Your Career'  status=coming-soon
- key=`aip-ai-work-and-automation-realities`  title='AI, Jobs, and Your Career'  status=coming-soon
- key=`aip-computer-vision-in-daily-life`  title='How AI Sees Your World'  status=coming-soon
- key=`aip-deepfakes-and-synthetic-media`  title='Deepfakes and Synthetic Media'  status=coming-soon
- key=`aip-explainable-ai`  title='Making AI Explainable'  status=coming-soon
- key=`aip-future-of-work-ai`  title="AI's Impact on Future Work"  status=coming-soon
- key=`aip-human-ai-interaction`  title='Human-AI Interaction Design'  status=coming-soon
- key=`aip-sustainable-ai`  title='Sustainable and Green AI'  status=coming-soon
- key=`aip-what-ai-knows-about-you`  title='AI Knows More Than You Think'  status=coming-soon
- key=`am-2`  title='Multimodal Models'  status=coming-soon
- key=`am-3`  title='Reinforcement Learning & Decision Models'  status=coming-soon
- key=`am-6`  title='Image Generation Models'  status=coming-soon
- key=`am-7`  title='Model Evaluation and Benchmarks'  status=coming-soon
- key=`am-8`  title='The Alignment Problem'  status=live
- key=`ap-1`  title='Voice and Real-Time AI'  status=coming-soon
- key=`ap-4`  title='The Context Window Race'  status=coming-soon
- key=`ap-5`  title='The Reasoning Revolution'  status=coming-soon
- key=`ap-6`  title='AI in Science'  status=coming-soon
- key=`ap-8`  title='Multimodal Breakthroughs'  status=coming-soon
- key=`ap-9`  title="What's Coming Next"  status=coming-soon
- key=`ar-11`  title='Performing Arts and AI'  status=coming-soon
- key=`ar-12`  title='Storytelling with AI'  status=coming-soon
- key=`ar-2`  title='AI in Game Design II'  status=coming-soon
- key=`ar-3`  title='AI in Game Design III'  status=coming-soon
- key=`ar-4`  title='AI Video Production'  status=coming-soon
- key=`ar-5`  title='Prompt Craft for Visual Art'  status=coming-soon
- key=`ar-6`  title='AI and Architecture'  status=coming-soon
- key=`ar-7`  title='AI Music Composition'  status=coming-soon
- key=`ar-9`  title="AI and the Writer's Voice"  status=coming-soon
- key=`bu-10`  title='Procurement and Vendor Evaluation'  status=coming-soon
- key=`bu-11`  title='AI for Small Business Managers'  status=live
- key=`bu-12`  title="AI's Impact on Jobs"  status=live
- key=`bu-6`  title='AI for Product Development'  status=coming-soon
- key=`bu-8`  title='AI for Finance and Operations'  status=coming-soon
- key=`bu-9`  title='AI in Customer Service'  status=coming-soon
- key=`cp-placeholder`  title='Welcome to the Course Catalog'  status=coming-soon
- key=`cp18`  title='The Future of Intelligence'  status=coming-soon
- key=`cp19`  title='AI in Social Media'  status=live
- key=`dv-11`  title='Working with the OpenAI API'  status=coming-soon
- key=`dv-12`  title='Fine-Tuning Language Models'  status=coming-soon
- key=`dv-18`  title='Building Production Agents with Vertex AI'  status=coming-soon
- key=`dv-19`  title='Agentic Data Workflows on Google Cloud'  status=coming-soon
- key=`dv-20`  title='AI &amp; Climate'  status=coming-soon
- key=`dv-21`  title="Don't Get Fooled: AI and Lies"  status=coming-soon
- key=`dv-22`  title='Understanding AI Bias and Fairness'  status=coming-soon
- key=`dv-23`  title='AI Ethics &amp; Decision-Making'  status=coming-soon
- key=`dv-24`  title='AI Governance'  status=coming-soon
- key=`dv-25`  title='AI in Society'  status=coming-soon
- key=`dv-26`  title='Building Production Agents with Vertex AI'  status=coming-soon
- key=`dv-27`  title='Building with AI'  status=coming-soon
- key=`dv-28`  title='Coded Unfair: AI Bias Exposed'  status=coming-soon
- key=`dv-29`  title='How Large Language Models Work'  status=coming-soon
- key=`dv-30`  title='Make It Yours: Create With AI'  status=coming-soon
- key=`dv-31`  title='The Context Window Race'  status=coming-soon
- key=`dv-32`  title='The Future of Intelligence'  status=coming-soon
- key=`dv-33`  title='Agentic Data Workflows on Google Cloud'  status=coming-soon
- key=`dv-34`  title="What's Really Inside AI?"  status=coming-soon
- key=`dv-35`  title='Make Something Real with AI'  status=coming-soon
- key=`dv-6`  title='AI App Architecture'  status=coming-soon
- key=`dv-8`  title='Deploying and Monitoring AI'  status=coming-soon

## courses.html Mega-Menu vs Disk

**61 `--live` buttons whose slug could not be auto-resolved**
(manual lookup needed — no slug in data-panel and CTA not inspected):
- panel=`am-1`  name=`GPT vs. Claude vs. Gemini`
- panel=`am-4`  name=`Running Models Locally`
- panel=`am-5`  name=`How Large Language Models Work`
- panel=`am-8`  name=`The Alignment Problem`
- panel=`am-9`  name=`Conversational AI and Chatbots`
- panel=`ap-10`  name=`Autonomous AI Systems`
- panel=`ap-2`  name=`The Hardware Race`
- panel=`ap-3`  name=`Synthetic Data and Self-Improvement`
- panel=`ap-4`  name=`The Context Window Race`
- panel=`ap-7`  name=`AI Agents in the Wild`
- panel=`ar-1`  name=`AI in Game Design I`
- panel=`ar-10`  name=`Photography and AI`
- panel=`ar-8`  name=`AI for Graphic Design`
- panel=`bu-1`  name=`AI Tools for Solo Founders`
- panel=`bu-11`  name=`AI for Small Business Managers`
- panel=`bu-12`  name=`AI's Impact on Jobs`
- panel=`bu-13`  name=`AI, Work, and Your Career`
- panel=`bu-2`  name=`AI for Marketing and Growth`
- panel=`bu-3`  name=`AI Risk for Business Leaders`
- panel=`bu-4`  name=`Funding and Pitching AI Ventures`
- panel=`bu-5`  name=`AI and the Future of Work`
- panel=`bu-7`  name=`Building an AI-First Business`
- panel=`cp1`  name=`AI Governance`
- panel=`cp10`  name=`AI & Finance`
- panel=`cp11`  name=`AI Psychology & Behavior`
- panel=`cp13`  name=`Applied AI Development`
- panel=`cp14`  name=`AI Leadership`
- panel=`cp15`  name=`AI & Media`
- panel=`cp15b`  name=`AI in Social Media`
- panel=`cp16`  name=`AI & National Security`
- panel=`cp17`  name=`AI Consciousness & Philosophy`
- panel=`cp18`  name=`The Future of Intelligence`
- panel=`cp19`  name=`AI in Social Media`
- panel=`cp2`  name=`AI in Society`
- panel=`cp20`  name=`AI and Misinformation`
- panel=`cp3`  name=`AI & Creativity`
- panel=`cp4`  name=`AI Ethics & Decision-Making`
- panel=`cp5`  name=`Building with AI`
- panel=`cp6`  name=`AI Careers & Research`
- panel=`cp7`  name=`AI in Healthcare`
- panel=`cp8`  name=`AI & Education`
- panel=`cp9`  name=`AI & Climate`
- panel=`dv-1`  name=`Building AI Agents I — Use Cases`
- panel=`dv-10`  name=`Working with the Anthropic API`
- panel=`dv-13`  name=`AI Security and Red-Teaming`
- panel=`dv-14`  name=`Evaluation and Testing for AI`
- panel=`dv-15`  name=`AI Code Review Fundamentals`
- panel=`dv-16`  name=`Security Auditing for AI-Generated Code`
- panel=`dv-17`  name=`Code Audit Workflows and Team Standards`
- panel=`dv-18`  name=`Building Production Agents with Vertex AI`
- panel=`dv-19`  name=`Agentic Data Workflows on Google Cloud`
- panel=`dv-2`  name=`Building AI Agents II — Skills`
- panel=`dv-26`  name=`Building Production Agents with Vertex AI`
- panel=`dv-27`  name=`Building with AI`
- panel=`dv-3`  name=`Building AI Agents III — Tools`
- panel=`dv-33`  name=`Agentic Data Workflows on Google Cloud`
- panel=`dv-36`  name=`Say It Right: Talk to AI`
- panel=`dv-4`  name=`Building AI Agents IV — OpenClaw`
- panel=`dv-5`  name=`Building AI Agents V — Optimization`
- panel=`dv-7`  name=`Prompt Engineering for Developers`
- panel=`dv-9`  name=`RAG Systems from Scratch`

**0 `--live` buttons resolved to a slug not found on disk:**
- _(none)_

**58 disk courses not represented by an auto-resolvable `--live` button:**
(some may have a button whose panel id couldn't be traced to a slug — cross-check against the unresolved list above)
- `ai-agents-in-the-wild`
- `ai-and-climate`
- `ai-and-creativity`
- `ai-and-education`
- `ai-and-finance`
- `ai-and-media`
- `ai-and-national-security`
- `ai-and-the-future-of-work`
- `ai-autonomous-systems`
- `ai-careers-and-research`
- `ai-code-review-fundamentals`
- `ai-consciousness-and-philosophy`
- `ai-ethics`
- `ai-for-graphic-design`
- `ai-for-marketing-and-growth`
- `ai-for-small-business-managers`
- `ai-governance`
- `ai-in-game-design-i`
- `ai-in-healthcare`
- `ai-in-society`
- `ai-job-market-impact`
- `ai-leadership`
- `ai-misinformation`
- `ai-psychology-and-behavior`
- `ai-risk-for-business-leaders`
- `ai-security-and-red-teaming`
- `ai-social-media`
- `ai-tools-for-solo-founders`
- `ai-work-and-automation-realities`
- `applied-ai-development`
- `building-agents-vertex-ai`
- `building-ai-agents-i-use-cases`
- `building-ai-agents-ii-skills`
- `building-ai-agents-iii-tools`
- `building-ai-agents-iv-openclaw`
- `building-ai-agents-v-optimization`
- `building-an-ai-first-business`
- `building-with-ai`
- `code-audit-workflows-team-standards`
- `conversational-ai-chatbots`
- `creating-with-ai-tools`
- `evaluation-and-testing-for-ai`
- `funding-and-pitching-ai-ventures`
- `gpt-vs-claude-vs-gemini`
- `how-large-language-models-work`
- `photography-and-ai`
- `prompt-engineering-for-developers`
- `rag-systems-from-scratch`
- `running-models-locally`
- `security-auditing-ai-generated-code`
- `synthetic-data-and-self-improvement`
- `talking-to-ai-prompt-writing`
- `the-alignment-problem`
- `the-context-window-race`
- `the-future-of-intelligence`
- `the-hardware-race`
- `vertex-ai-data-agents`
- `working-with-the-anthropic-api`

## courses.html Panels

Total panels (by `dv-N` id): **30**, with `core-badge-live`: **73**.

_Panels don't encode a course slug, so direct panel↔disk matching isn't implemented in this audit._
_Titles in each panel are listed below for human cross-reference with the nav and disk lists above._

### 14 panels with live badge
- `dv-1`  'Building AI Agents I — Use Cases'
- `dv-2`  'Building AI Agents II — Skills'
- `dv-3`  'Building AI Agents III — Tools'
- `dv-4`  'Building AI Agents IV — OpenClaw'
- `dv-5`  'Building AI Agents V — Optimization'
- `dv-7`  'Prompt Engineering for Developers'
- `dv-9`  'RAG Systems from Scratch'
- `dv-10`  'Working with the Anthropic API'
- `dv-13`  'AI Security and Red-Teaming'
- `dv-14`  'Evaluation and Testing for AI'
- `dv-15`  'AI Code Review Fundamentals'
- `dv-16`  'Security Auditing for AI-Generated Code'
- `dv-17`  'Code Audit Workflows and Team Standards'
- `dv-36`  'Say It Right: Talk to AI'

### 16 panels without live badge
- `dv-20`  'AI & Climate'
- `dv-21`  "Don't Get Fooled: AI and Lies"
- `dv-22`  'Understanding AI Bias and Fairness'
- `dv-23`  'AI Ethics & Decision-Making'
- `dv-24`  'AI Governance'
- `dv-25`  'AI in Society'
- `dv-26`  'Building Production Agents with Vertex AI'
- `dv-27`  'Building with AI'
- `dv-28`  'Coded Unfair: AI Bias Exposed'
- `dv-29`  'How Large Language Models Work'
- `dv-30`  'Make It Yours: Create With AI'
- `dv-31`  'The Context Window Race'
- `dv-32`  'The Future of Intelligence'
- `dv-33`  'Agentic Data Workflows on Google Cloud'
- `dv-34`  "What's Really Inside AI?"
- `dv-35`  'Make Something Real with AI'

## dashboard.html vs Disk

**0 disk courses missing from dashboard COURSES array:**
- _(none)_

**2 dashboard entries with no disk folder:**
- `ai-careers`
- `ai-foundations`

## stats.json vs Disk

stats.json reports **54** live; disk has **63**.  Delta: **-9**

## i18n Course Files

- `courses.ar.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.de.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.en.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.es.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.fa.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.fr.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.hi.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.ja.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.ko.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.ru.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.sw.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.ur.json`: 1518 titles (disk title-guesses missing: 8)
- `courses.zh.json`: 1518 titles (disk title-guesses missing: 8)

_(i18n comparison uses extracted title guesses from m1.html; some titles are garbage strings like '🎯 Advanced' — human review needed.)_

## Disk Courses With Bad Title Extraction

These folders have m1.html but the lesson-kicker regex returned a non-title string.
Canonical title will need to be set elsewhere (registry, or a manual list).

- `ai-and-finance` → '🎯 Advanced'
- `evaluation-and-testing-for-ai` → 'Lesson 1'
