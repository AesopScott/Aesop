# i18n Catalogs — AESOP AI Academy

Per-language JSON translation catalogs for pages that ship in multiple languages.

## Files

- `courses.en.json` — canonical English catalog (auto-generated; do not hand-edit)
- `courses.{lang}.json` — translation catalogs, keyed by the English source string

Supported languages follow Mod Gen: **es, fr, de, hi, ur, zh, fa, ru, ko, ja, ar, sw**.
RTL handling (dir="rtl") is auto-applied for `ar`, `ur`, `fa`.

## How it works

Each catalog is a flat `{ "English string": "Translated string" }` map. At build time
the English source HTML is walked, every translatable string is located at its byte
offset, and if the catalog has a non-identical value that string is substituted in
place. Byte-safe — any string not translated falls through untouched.

Translatable content:

- Visible text nodes (outside `<script>` / `<style>` / `<noscript>`)
- Attribute values for `alt`, `title`, `aria-label`, `placeholder`
- `<meta name="description"|"keywords" content="...">`
- `<html lang="...">` (auto-set to target language)

Site-internal links starting with `/ai-academy/...` are rewritten to `/{lang}/ai-academy/...`.

## Workflow

1. **Re-extract** when English `courses.html` changes:

   ```bash
   python3 scripts/i18n_extract.py ai-academy/courses.html i18n/courses.en.json
   ```

   New English strings appear in `courses.en.json`. Merge them into each language
   catalog manually — just paste the new keys in (with English as placeholder value)
   then fill in translations.

2. **Translate** by editing the per-language JSON. Keys MUST remain unchanged. Values
   can be any string; leave equal to the English key to fall through to English.

3. **Build** any single language:

   ```bash
   python3 scripts/i18n_build.py es ai-academy/courses.html es/ai-academy/courses.html
   ```

4. **Build all** languages in one shot:

   ```bash
   bash scripts/i18n_build_all.sh
   ```

## Extending to new pages

The same scripts work on any HTML source. For a new page:

```bash
python3 scripts/i18n_extract.py ai-academy/foo.html i18n/foo.en.json
# copy foo.en.json to foo.{lang}.json for each language, translate
bash scripts/i18n_build_all.sh ai-academy/foo.html
```

## Extending to new languages

Add the code to `LANGS=(...)` in `scripts/i18n_build_all.sh`, copy any existing catalog
to `courses.{newcode}.json`, translate. If the new language is RTL, add it to
`RTL_LANGS` at the top of `scripts/i18n_build.py`.
