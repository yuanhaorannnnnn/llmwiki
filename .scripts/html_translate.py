#!/usr/bin/env python3
"""Translate text nodes in HTML while preserving all tags, classes, styles, and layout.

Usage:
  python3 html_translate.py URL [--selector CSS_SELECTOR] [--api claude|google]
  python3 html_translate.py FILE.html

Requirements: pip install beautifulsoup4
For --api google: pip install deep-translator
"""

import sys, os, re, json, argparse
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser

try:
    from bs4 import BeautifulSoup, NavigableString, Comment
except ImportError:
    print("Error: pip install beautifulsoup4")
    sys.exit(1)

# ── text extraction ──────────────────────────────────────────────
SKIP_TAGS = {'script', 'style', 'noscript', 'code', 'pre', 'kbd', 'var', 'samp', 'svg', 'math'}

def is_translatable(text):
    """Only translate text that has actual linguistic content."""
    t = text.strip()
    if not t:
        return False
    if re.match(r'^[\s\d!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+$', t):
        return False
    if re.match(r'^[A-Za-z0-9_\-./:@]+$', t):  # URLs, paths, IDs
        return False
    return True

def extract_texts(soup, selector=None):
    """Walk the DOM and collect translatable text nodes."""
    entries = []
    root = soup.select_one(selector) if selector else soup
    if root is None:
        print(f"Warning: selector '{selector}' matched nothing, using whole document")
        root = soup
    for el in root.descendants:
        if isinstance(el, NavigableString) and not isinstance(el, Comment):
            if el.parent and el.parent.name in SKIP_TAGS:
                continue
            if is_translatable(str(el)):
                entries.append(el)
    return entries

# ── translate backend ────────────────────────────────────────────
def build_prompt(texts):
    """Build a single prompt for batch translation."""
    items = "\n".join(f"[{i}] {t}" for i, t in enumerate(texts))
    return f"Translate each numbered item below to Chinese. Keep all technical terms in English. Output ONLY the translations, one per line, in the format [N] translation:\n\n{items}"

def parse_batch_response(response, count):
    """Parse batch translation output back into a list."""
    translations = {}
    for line in response.strip().split('\n'):
        m = re.match(r'\[(\d+)\]\s*(.+)', line.strip())
        if m:
            idx = int(m.group(1))
            translations[idx] = m.group(2).strip()
    result = []
    for i in range(count):
        result.append(translations.get(i, ""))
    return result

def translate_google(texts, source='en', target='zh-CN'):
    """Batch translate using Google Translate (free, via deep-translator)."""
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("Error: pip install deep-translator")
        sys.exit(1)

    combined = "\n|||SEP|||\n".join(texts)
    translator = GoogleTranslator(source=source, target=target)
    result = translator.translate(combined)
    return result.split("\n|||SEP|||\n")

def translate_with_llm(texts, source='en', target='zh-CN'):
    """Batch translate using an LLM. Override this with your preferred API."""
    prompt = build_prompt(texts)
    # Write prompt for external processing
    with open('/tmp/html_translate_prompt.txt', 'w') as f:
        f.write(prompt)
    raise NotImplementedError(
        "LLM translation requires API integration. "
        "For now, prompt written to /tmp/html_translate_prompt.txt. "
        "Paste the translations to /tmp/html_translate_result.txt, one per line, "
        "then re-run with --result-file."
    )

# ── main ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Translate HTML text nodes, preserving structure")
    parser.add_argument('source', help='URL or local HTML file')
    parser.add_argument('--output', '-o', help='Output file (default: source-zh.html)')
    parser.add_argument('--selector', help='CSS selector to limit translation scope')
    parser.add_argument('--api', choices=['claude', 'google'], default='claude',
                        help='Translation API (default: claude)')
    parser.add_argument('--result-file', help='Pre-translated results file (one per line)')
    parser.add_argument('--source-lang', default='en')
    parser.add_argument('--target-lang', default='zh-CN')
    args = parser.parse_args()

    # 1. Load HTML
    if args.source.startswith('http://') or args.source.startswith('https://'):
        req = Request(args.source, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8')
        except URLError as e:
            print(f"Error fetching URL: {e}")
            sys.exit(1)
    else:
        with open(args.source) as f:
            html = f.read()

    soup = BeautifulSoup(html, 'lxml')

    # 2. Extract translatable text nodes
    entries = extract_texts(soup, args.selector)
    if not entries:
        print("No translatable text found.")
        sys.exit(0)

    texts = [str(e) for e in entries]
    print(f"Found {len(texts)} translatable text nodes ({sum(len(t) for t in texts)} chars)")

    # 3. Translate
    if args.result_file:
        with open(args.result_file) as f:
            translations = [line.rstrip('\n') for line in f if line.strip()]
    elif args.api == 'google':
        translations = translate_google(texts, args.source_lang, args.target_lang)
    else:
        # Write prompt for external LLM processing
        prompt = build_prompt(texts)
        prompt_file = '/tmp/html_translate_prompt.txt'
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        print(f"\nPrompt written to {prompt_file}")
        print(f"Copy this file content to your LLM, then save translations to /tmp/html_translate_result.txt")
        print(f"Then re-run: python3 {sys.argv[0]} {' '.join(sys.argv[1:])} --result-file /tmp/html_translate_result.txt\n")
        # Also print the texts directly for inline use
        for i, t in enumerate(texts):
            print(f"[{i}] {t[:120]}")
        sys.exit(0)

    if len(translations) != len(texts):
        print(f"Warning: got {len(translations)} translations but expected {len(texts)}")

    # 4. Replace text nodes in-place
    for i, (entry, translation) in enumerate(zip(entries, translations)):
        if translation and translation != str(entry):
            entry.replace_with(NavigableString(translation))

    # 5. Write output
    output_path = args.output
    if not output_path:
        base = re.sub(r'\.html?$', '', os.path.basename(args.source))
        output_path = f"{base}-zh.html"

    result = soup.prettify(encoding='utf-8')
    with open(output_path, 'wb') as f:
        f.write(result)

    print(f"Done → {output_path}")

if __name__ == '__main__':
    main()
