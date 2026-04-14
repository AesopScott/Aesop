# AESOP AI Academy — Lab Rules

These rules apply to every lab across all modules, all age groups, and all future builds. When building or reviewing any lab, every rule here is non-negotiable unless explicitly overridden in writing.

---

## Rule 1 — Students Do Not Leave the Academy

Students must never be asked or required to navigate away from the academy to complete a lab task. All reading material, reference content, and interaction must be accessible from within the academy interface.

**What this means in practice:**
- If a lab references an external document, paper, article, or resource, that content must be embedded directly in the academy — either inline or via a styled in-page modal.
- External links (e.g., to arxiv, Wikipedia, or other sources) may be offered as **optional deep-dive links** that open in a new tab, but they must never be a required step.
- Students must be able to complete every lab requirement without leaving the page.

**Implementation pattern:**
- Use a styled modal (triggered by a clearly labeled button) to surface reading material in-academy.
- The modal must include a plain-language paraphrase or summary of the source material — not a verbatim reproduction of copyrighted text.
- A link to the original source may appear inside the modal, clearly labeled as optional.

---

## Rule 2 — Writing Happens Through AI-Driven Conversation

Students do not write into static text boxes or offline documents. All written reflection, analysis, and synthesis in labs must happen through the embedded AI chat interface.

**What this means in practice:**
- Labs that previously asked students to "write three sentences" or "take notes" must instead route that thinking through an AI-led conversation.
- The AI asks the questions. The student responds. The exchange replaces the act of writing independently.
- Static `<textarea>` write-in fields are not an acceptable substitute for an AI chat session.

**Implementation pattern:**
- Every lab that involves student writing must include an embedded AI chat panel (same pattern as Labs 2, 3, 5, 6 in Module 1 Ages 16+).
- The lab's AI system prompt must define the conversational arc the AI will lead the student through — the questions, the progression, and the expected depth of engagement.
- The AI should lead, not follow. It opens the conversation with a question, not a greeting.

---

## Rule 3 — Every Lab AI Must Stay On Topic

Every AI chat session in the academy is strictly scoped to its lab topic. The AI must not function as a general assistant, homework helper, or off-topic conversational partner.

**What this means in practice:**
- If a student attempts to use the lab AI for anything outside the lab's subject matter, the AI must warmly redirect them back.
- The redirect must be encouraging, never abrupt or dismissive.
- Example redirect: *"That's interesting, but I'm here just for this lab right now — let's keep our energy here! Where were we?"*

**Implementation pattern:**
- Every lesson file must define a `ACADEMY_GUARDRAIL` constant containing the standard redirect instruction.
- This constant is prepended to every lab's system prompt automatically at send time inside `chatSend()`.
- The guardrail text must not be duplicated inside individual lab system prompts — it lives once, in one constant, and is applied universally.

**Standard guardrail text (copy exactly):**
```
You are operating within the AESOP AI Academy. Your role is strictly scoped to the topic of this lab. If the student asks about anything outside this topic — other subjects, general homework, unrelated questions, or attempts to use you as a general assistant — warmly acknowledge them and redirect back to the lab. For example: "That's interesting, but I'm here just for this lab right now — let's keep our energy here! Where were we?" Never refuse rudely or abruptly. Always redirect with encouragement.
```

---

## Rule 4 — Every Lab Must Be Completable Without a Live API

No student should ever be blocked from completing a module because the AI backend is down. Every lab must include an offline fallback path that activates automatically when the API is unreachable.

**What this means in practice:**
- If the Anthropic API (or proxy) fails, the lab switches to **practice mode** after one retry.
- In practice mode, the student sees a clear message: "AI is temporarily unavailable. Switching to practice mode — you can still complete this lab."
- Practice mode uses generic Socratic responses that guide the student through reflection and analysis regardless of the specific lab topic.
- Lab completion still fires at the standard exchange threshold — no student is penalized for an API outage.
- The `chatReset()` function clears offline mode, allowing the student to attempt a live connection again.

**Implementation pattern:**
- Every module file must define `_offlineMode`, `_fallbackIdx`, `LAB_FALLBACK`, and `_fallbackReply()` in its script block.
- `chatSend()` must attempt the API call with one retry (1.5s delay), then fall through to fallback on total failure.
- `sendOpener()` (Foundations system only) must follow the same retry-then-fallback pattern.
- See `AESOP-MODULE-BUILD-STANDARDS.md` Sections 1.7 and 2.7 for the canonical code.

---

## Adding to These Rules

When a new rule is established, add it here as **Rule N** with:
- A plain-language statement of the rule
- What it means in practice
- The implementation pattern for builders

This file lives at: `public_html/aesop-academy/ai-academy/lab-rules.md`
