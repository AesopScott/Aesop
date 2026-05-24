# Aesop Academy Catalog API Update

**Date:** May 24, 2026  
**Issue:** Course URLs in catalog API were incorrect  
**Status:** Fixed and deployed  

---

## What Happened

The Aesop Academy course catalog API (`/aesop-api/catalog.php`) was generating incorrect course URLs missing the `/modules/` directory segment. This caused all course links sent to 25experts.com to fail, redirecting users to the home page instead of the intended course.

### Example
- **Incorrect (old):** `https://aesopacademy.org/ai-academy/electives-hub.html?course=prompt-engineering-for-developers`
- **Correct (new):** `https://aesopacademy.org/ai-academy/modules/electives-hub.html?course=prompt-engineering-for-developers`

---

## Root Cause

The catalog API was constructing course hub URLs without the correct directory path. This affected all V1 (version 1) courses served through the electives hub.

---

## What We Fixed

**File:** `aesop-api/catalog.php`  
**Change:** Added `/modules/` to the course URL construction for V1 courses

```php
// Before
'https://aesopacademy.org/ai-academy/electives-hub.html?course={id}'

// After
'https://aesopacademy.org/ai-academy/modules/electives-hub.html?course={id}'
```

**Deployment:** Committed to main branch and live as of 2026-05-24

---

## What You Need to Do

### Step 1: Refresh Your Catalog Cache
The catalog API now generates URLs with the correct path structure. The `catalog_hash` value in the API response will have changed, which will trigger your change-detection logic.

**Fetch the updated catalog:**
```
GET https://aesopacademy.org/aesop-api/catalog.php
```

Your system should automatically detect the hash change and refresh your local cache with the corrected URLs.

### Step 2: Update Existing Course Links
If you have stored course URLs in your database or configuration from before this fix, you need to either:

**Option A (Recommended):** Delete any cached course data and re-fetch from the API. This ensures you always have the latest URLs.

**Option B:** Manually update all stored URLs to include `/modules/` in the path:
- Replace: `/ai-academy/electives-hub.html`
- With: `/ai-academy/modules/electives-hub.html`

### Step 3: Verify Links
After refreshing, test a few course links to confirm they resolve correctly:
- Example: `https://aesopacademy.org/ai-academy/modules/electives-hub.html?course=prompt-engineering-for-developers`
- Should load the course page, not redirect to home

---

## API Details

### Catalog Endpoint
- **URL:** `https://aesopacademy.org/aesop-api/catalog.php`
- **Method:** GET
- **CORS:** Enabled (`Access-Control-Allow-Origin: *`)

### Response Structure
```json
{
  "catalog_hash": "sha256-hash-of-courses-data",
  "generated_at": "2026-05-24T...",
  "courses": [
    {
      "id": "course-id",
      "name": "Course Name",
      "desc": "Short description",
      "url": "https://aesopacademy.org/ai-academy/modules/electives-hub.html?course=course-id",
      "live": true
    }
  ]
}
```

### Course URL Formats
- **V1 courses** (standard): `/ai-academy/modules/electives-hub.html?course={id}`
- **V2 courses** (newer format): `/ai-academy/modules/v2/{slug}/m1.html`

---

## Questions?

If you encounter any issues with the updated catalog or course links, please reach out with:
- Specific course IDs that aren't working
- Error messages or behavior you're seeing
- Screenshots of the problem (if applicable)

We're here to help ensure a smooth transition!

---

**Aesop Academy Team**
