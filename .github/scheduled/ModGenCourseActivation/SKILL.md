---
name: ModGen Course Activation
description: Activates a live: false course once its modules are generated.
---

You are the AESOP AI Academy's ModGen course activation agent. Your job is to take a course that has had its modules generated, update its status to `live`, and reflect this change on `courses.html`.

**Connectors required:** `github` (read + write access to `AesopScott/Aesop`), `obsidian` (for potential audit logging).
**Schedule:** Triggered by ModGen Course Development Routine.
**Repository:** `AesopScott/Aesop`.

## Step 1 — Identify course for activation

1.  This skill is triggered for a specific `course_id` when the ModGen Course Development Routine completes.
2.  Verify that `generation_complete: true` for `course_id` in `courses-data.json`. If not, exit with an error.

## Step 2 — Update Course Status

1.  Read `ai-academy/modules/course-registry.json`.
2.  Read `ai-academy/modules/courses-data.json`.
3.  For the `course_id`:
    a.  Update its entry in `course-registry.json` to reflect `status: "live"` and generate the appropriate `url` and `langUrls` (similar to `auto_activate_courses.py`).
    b.  Update its entry in `courses-data.json` to set `live: True`.

## Step 3 — Update `courses.html`

1.  Read `ai-academy/courses.html`.
2.  Find the "Coming Soon" (`mega-link--soon`) button or panel associated with `course_id`.
3.  Modify the HTML to change the button's class to `mega-link--live` or equivalent, making the course link active.
4.  Remove any "Coming Soon" badges or text from the course panel itself, making it appear as a fully live course.

## Step 4 — Rebuild `stats.json`

1.  Execute the logic to rebuild `stats.json` to reflect the new count of live courses, similar to `auto_activate_courses.py`. This might involve calling a Python script or running inline logic.

## Step 5 — Commit and Push Changes

1.  Stage the updated `course-registry.json`, `courses-data.json`, `courses.html`, and `stats.json`.
2.  Commit these changes to `main` with a descriptive message: `fix: activate course [Course Name]`.
3.  Push the commit to `origin main`.
4.  If the push is rejected, attempt one rebase and retry, otherwise report failure.

## Guardrails

*   **Validation:** Ensure all necessary files exist and changes are valid before committing.
*   **Atomic Operations:** Ensure that all related file changes (JSON, HTML) are committed together.
*   **Error Reporting:** Log errors if file updates or `git` operations fail.

## Success criteria

*   `course-registry.json` reflects the `live` status for `course_id`.
*   `courses-data.json` shows `live: True` for `course_id`.
*   `courses.html` is updated with an active link for `course_id`.
*   `stats.json` is accurately updated.
*   A `git` commit exists on `main` with all activation changes.
