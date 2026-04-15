#!/usr/bin/env python3
"""Build a translated HTML page from a canonical English source + a language catalog.

Usage:
    python3 scripts/i18n_build.py <lang> <source_html> <output_html> [catalog_dir]

Example:
    python3 scripts/i18n_build.py es ai-academy/courses.html es/ai-academy/courses.html

Reads i18n/<basename>.<lang>.json, identifies translatable string offsets in the
source HTML using html.parser, then performs byte-safe offset substitution so the
output is identical to the source except where translations are applied.

Features:
    - Preserves all HTML structure, inline CSS, scripts, whitespace (byte-safe)
    - Replaces text nodes + translatable attribute values (alt, title, aria-label, placeholder)
    - Replaces <meta name="description|keywords" content="...">
    - Updates <html lang="en"> -> <html lang="XX"> and adds dir="rtl" for RTL langs
    - Missing translations fall back to English silently
    - Idempotent — rerunning regenerates the same output from the canonical source
"""
import json, sys, re, pathlib
from html.parser import HTMLParser

SKIP_TAGS = {'script', 'style', 'noscript'}
TRANSLATABLE_ATTRS = {'alt', 'title', 'aria-label', 'placeholder'}
RTL_LANGS = {'ar', 'ur', 'fa', 'he'}


class OffsetFinder(HTMLParser):
    """Walk HTML and record (start, end, original_text, kind) triples for each translatable string."""
    def __init__(self, html_text):
        super().__init__(convert_charrefs=False)
        self.html = html_text
        self.stack = []
        self.spans = []  # list of (start, end, text, kind)
        self.html_tag_span = None  # (start_of_open_tag, end_of_open_tag) for <html ...>

    def _find_attr_value(self, tag_start, attr_name, attr_value):
        """Find byte offsets of the attribute value within the tag open."""
        # Find end of this tag's open bracket
        tag_end = self.html.find('>', tag_start)
        if tag_end < 0:
            return None
        chunk = self.html[tag_start:tag_end + 1]
        # Match attr="value" or attr='value'
        esc = re.escape(attr_name)
        for m in re.finditer(rf'\b{esc}\s*=\s*(["\'])(.*?)\1', chunk, re.S):
            if m.group(2) == attr_value:
                val_start = tag_start + m.start(2)
                val_end = tag_start + m.end(2)
                return (val_start, val_end)
        return None

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        start = self.getpos_offset()
        if tag == 'html':
            # record open-tag span so we can manipulate lang / dir
            tag_end = self.html.find('>', start)
            if tag_end >= 0:
                self.html_tag_span = (start, tag_end + 1)

        meta_name = None
        if tag == 'meta':
            for k, v in attrs:
                if k == 'name':
                    meta_name = (v or '').lower()

        for k, v in attrs:
            if not v:
                continue
            if k in TRANSLATABLE_ATTRS:
                span = self._find_attr_value(start, k, v)
                if span:
                    self.spans.append((span[0], span[1], v, 'attr'))
            elif tag == 'meta' and k == 'content' and meta_name in ('description', 'keywords'):
                span = self._find_attr_value(start, k, v)
                if span:
                    self.spans.append((span[0], span[1], v, 'attr'))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if any(t in SKIP_TAGS for t in self.stack):
            return
        if not data.strip():
            return
        start = self.getpos_offset()
        end = start + len(data)
        # For each non-empty line inside this data block, record its offsets
        off = 0
        for line in re.split(r'(\n)', data):
            if line == '\n' or not line.strip():
                off += len(line)
                continue
            stripped = line.strip()
            # find stripped within line to get leading ws length
            lead = len(line) - len(line.lstrip())
            s_start = start + off + lead
            s_end = s_start + len(stripped)
            self.spans.append((s_start, s_end, stripped, 'text'))
            off += len(line)

    def getpos_offset(self):
        """Byte offset of current parser position in self.html."""
        line, col = self.getpos()
        # Compute offset from line/col (line is 1-indexed)
        # Cache line starts
        if not hasattr(self, '_line_starts'):
            starts = [0]
            for i, ch in enumerate(self.html):
                if ch == '\n':
                    starts.append(i + 1)
            self._line_starts = starts
        return self._line_starts[line - 1] + col


def build(lang, src, dst, catalog_dir='i18n'):
    src_name = pathlib.Path(src).stem
    catalog_path = pathlib.Path(catalog_dir) / f'{src_name}.{lang}.json'
    if not catalog_path.exists():
        print(f'Catalog missing: {catalog_path}')
        sys.exit(2)
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    finder = OffsetFinder(html)
    finder.feed(html)

    # Build replacements: list of (start, end, replacement_text)
    replacements = []
    translated_count = 0
    for start, end, text, kind in finder.spans:
        tr = catalog.get(text)
        if tr and tr != text:
            if kind == 'attr':
                # Escape for attribute value context
                rep = tr.replace('&', '&amp;').replace('"', '&quot;')
            else:
                rep = tr
            replacements.append((start, end, rep))
            translated_count += 1

    # Add <html lang="..."> and optional dir="rtl" rewrite
    if finder.html_tag_span:
        ts, te = finder.html_tag_span
        open_tag = html[ts:te]
        new_tag = re.sub(r'\blang\s*=\s*(["\'])[^"\']*\1', f'lang="{lang}"', open_tag)
        if new_tag == open_tag and 'lang=' not in open_tag:
            new_tag = open_tag[:-1] + f' lang="{lang}">'
        if lang in RTL_LANGS and 'dir=' not in new_tag:
            new_tag = new_tag[:-1] + ' dir="rtl">'
        if new_tag != open_tag:
            replacements.append((ts, te, new_tag))

    # Apply replacements right-to-left so offsets stay valid
    replacements.sort(key=lambda r: r[0], reverse=True)
    out = html
    for start, end, rep in replacements:
        out = out[:start] + rep + out[end:]

    # Note: no automatic link rewriting. Built pages live at
    # ai-academy/modules/{lang}/<relpath>, so absolute "/ai-academy/..." hrefs in
    # the English source are left intact (they point at the canonical English
    # sibling pages). If/when per-language targets exist, rewrite here.

    pathlib.Path(dst).parent.mkdir(parents=True, exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'Built {dst} ({lang}): {translated_count}/{len(catalog)} strings translated')


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    build(sys.argv[1], sys.argv[2], sys.argv[3],
          sys.argv[4] if len(sys.argv) > 4 else 'i18n')


if __name__ == '__main__':
    main()
