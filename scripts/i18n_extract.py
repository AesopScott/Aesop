#!/usr/bin/env python3
"""Extract translatable strings from a canonical English HTML page into an i18n catalog.

Usage:
    python3 scripts/i18n_extract.py ai-academy/courses.html i18n/courses.en.json

Produces a JSON object { "English source text": "English source text" } — the key
is the English string exactly as it appears on the page, and the initial value is
the same string (so the English catalog is a useful fallback / reference).

Non-English catalogs (courses.es.json, courses.fr.json, ...) are created by copying
this file and translating the VALUES only. Keys must not change.

What's extracted:
    - Visible text nodes (excluding contents of <script>, <style>, <noscript>)
    - Values of translatable attributes: alt, title, aria-label, placeholder
    - <meta name="description" content="..."> and <title> text
"""
import json, sys, re
from html.parser import HTMLParser

SKIP_TAGS = {'script', 'style', 'noscript'}
TRANSLATABLE_ATTRS = {'alt', 'title', 'aria-label', 'placeholder'}

class StringExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.strings = []   # ordered, may contain dupes — dedupe later preserving first occurrence
        self.seen = set()

    def _add(self, s):
        s = s.strip()
        if not s or s in self.seen:
            return
        # Filter: require at least one alpha char, min len 2
        if len(s) < 2:
            return
        if not any(c.isalpha() for c in s):
            return
        self.seen.add(s)
        self.strings.append(s)

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        for k, v in attrs:
            if k in TRANSLATABLE_ATTRS and v:
                self._add(v)
            elif tag == 'meta' and k == 'content':
                # Catch <meta name="description" content="..."> style
                d = dict(attrs)
                if d.get('name', '').lower() in ('description', 'keywords') and v:
                    self._add(v)

    def handle_startendtag(self, tag, attrs):
        for k, v in attrs:
            if k in TRANSLATABLE_ATTRS and v:
                self._add(v)
            elif tag == 'meta' and k == 'content':
                d = dict(attrs)
                if d.get('name', '').lower() in ('description', 'keywords') and v:
                    self._add(v)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if any(t in SKIP_TAGS for t in self.stack):
            return
        # Split on newlines for cleaner strings but preserve single-line phrases
        for line in data.splitlines():
            self._add(line)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    ex = StringExtractor()
    ex.feed(html)
    catalog = {s: s for s in ex.strings}
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"Extracted {len(catalog)} strings from {src} -> {dst}")


if __name__ == '__main__':
    main()
