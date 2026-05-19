#!/usr/bin/env python3
"""
Download an HTML e-book, translate text nodes, make it self-contained for offline browsing.

Workflow:
  1. Mirror all chapter pages via wget (downloads HTML + CSS + JS + fonts + images)
  2. Extract unique text nodes from all chapters
  3. Batch translate via Google Translate (free) or LLM
  4. Replace text nodes in-place (zero format change)
  5. Fix image paths → local images/
  6. Fix internal links → relative .html files
  7. Output: self-contained offline-ready translated HTMLs

Usage:
  python3 html_book_translate.py --chapters chapters.json --output ./output/
  python3 html_book_translate.py --base-url https://example.com/book --slugs slug1 slug2 ... --output ./output/

Requirements:
  pip install beautifulsoup4 deep-translator
  apt install wget
"""

import os, re, sys, json, time, shutil, argparse, subprocess, urllib.parse
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────
WGET_ARGS = [
    '--page-requisites', '--convert-links',
    '--no-directories', '--adjust-extension',
    '--timeout=15', '--tries=2', '-e', 'robots=off',
    '-U', 'Mozilla/5.0',
]

SKIP_TAGS = {'script', 'style', 'noscript', 'code', 'pre', 'kbd', 'var', 'samp', 'svg', 'math'}

# ── Step 1: Mirror pages ────────────────────────────────────────
def mirror_chapters(base_url, slugs, work_dir):
    """Download all chapter pages and their resources via wget."""
    os.makedirs(work_dir, exist_ok=True)
    for i, slug in enumerate(slugs):
        url = f"{base_url}/{slug}"
        print(f"[{i+1}/{len(slugs)}] wget {slug} ...", end=" ", flush=True)
        subprocess.run(
            ['wget'] + WGET_ARGS + ['-P', work_dir, url],
            capture_output=True, text=True, cwd=work_dir, timeout=120
        )
        files = [f for f in os.listdir(work_dir) if not f.startswith('.')]
        print(f"({len(files)} files)")

    # Remove .1 .2 suffix duplicates from wget --no-directories
    deleted = 0
    for fn in os.listdir(work_dir):
        if re.search(r'\.(js|css|woff2|png|jpg|webp)\.[0-9]+$', fn):
            os.remove(os.path.join(work_dir, fn))
            deleted += 1
    if deleted:
        print(f"Removed {deleted} duplicate files")

    # Fix .1 references in HTMLs
    for fn in os.listdir(work_dir):
        if not fn.endswith('.html'): continue
        fpath = os.path.join(work_dir, fn)
        with open(fpath) as f:
            html = f.read()
        fixed = re.sub(r'(\.(?:js|css|woff2|png|jpg|webp|svg|ico))\.1\b', r'\1', html)
        if fixed != html:
            with open(fpath, 'w') as f:
                f.write(fixed)

    return work_dir

# ── Step 2: Extract text nodes ───────────────────────────────────
def is_translatable(text):
    """Filter out numbers-only, symbols-only, URLs, etc."""
    t = text.strip()
    if len(t) < 2:
        return False
    if re.match(r'^[\s\d!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+$', t):
        return False
    return True

def extract_texts(html_dir):
    """Extract unique translatable text nodes from all HTMLs in a directory."""
    from bs4 import BeautifulSoup, NavigableString, Comment

    all_texts = []
    seen = set()
    for fn in sorted(os.listdir(html_dir)):
        if not fn.endswith('.html'): continue
        fpath = os.path.join(html_dir, fn)
        with open(fpath, 'rb') as f:
            html = f.read().decode('utf-8', errors='replace')
        soup = BeautifulSoup(html, 'lxml')
        for el in soup.descendants:
            if isinstance(el, NavigableString) and not isinstance(el, Comment):
                if el.parent and el.parent.name in SKIP_TAGS:
                    continue
                t = str(el)
                if is_translatable(t) and t not in seen:
                    seen.add(t)
                    all_texts.append(t)
    return all_texts

# ── Step 3: Translate ────────────────────────────────────────────
def translate_google(texts, source='en', target='zh-CN'):
    """Batch translate using Google Translate (free, via deep-translator)."""
    from deep_translator import GoogleTranslator

    batch_size = 50
    sep = "\n|||S|||\n"
    translations = {}
    done = 0

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        valid = [(i+j, t) for j, t in enumerate(batch) if t and len(t) > 1]
        if not valid: continue

        indices = [v[0] for v in valid]
        texts_batch = [v[1] for v in valid]
        combined = sep.join(texts_batch)

        for attempt in range(3):
            try:
                result = GoogleTranslator(source=source, target=target).translate(combined)
                parts = result.split(sep)
                if len(parts) == len(texts_batch):
                    for idx, trans in zip(indices, parts):
                        translations[idx] = trans
                    done += len(texts_batch)
                    break
                else:
                    time.sleep(1)
            except Exception:
                time.sleep(1)
        else:
            for idx, t in zip(indices, texts_batch):
                translations[idx] = t  # fallback to original

        pct = done / len(texts) * 100
        if (i // batch_size) % 10 == 0:
            print(f"  {done}/{len(texts)} ({pct:.0f}%)")

    # Fill gaps
    result = []
    for i in range(len(texts)):
        result.append(translations.get(i, texts[i]))
    return result

def translate_llm(texts, prompt_file='/tmp/html_book_translate_prompt.txt'):
    """Write translation prompt for external LLM processing."""
    with open(prompt_file, 'w') as f:
        f.write("Translate each numbered item to Simplified Chinese. Keep technical terms, proper names, and book titles in English. Output ONLY: [N] translation\n\n")
        for i, t in enumerate(texts):
            f.write(f"[{i}] {t}\n")
    print(f"Prompt written to {prompt_file}")
    print(f"Translate it with your LLM, save results (one '[N] translation' per line) to /tmp/html_book_translate_result.txt")
    print(f"Then re-run with --translation-file /tmp/html_book_translate_result.txt")
    sys.exit(0)

# ── Step 4 & 5: Rebuild ─────────────────────────────────────────
def rebuild(html_dir, output_dir, texts, translations, slug_to_file):
    """Replace text nodes, fix images, fix links, write output."""
    lookup = {}
    for orig, trans in zip(texts, translations):
        if trans and trans != orig:
            lookup[orig] = trans

    # Collect and download images
    img_dir = os.path.join(output_dir, 'images')
    os.makedirs(img_dir, exist_ok=True)

    all_images = {}  # original_path → local_filename
    for fn in sorted(os.listdir(html_dir)):
        if not fn.endswith('.html'): continue
        fpath = os.path.join(html_dir, fn)
        with open(fpath, 'rb') as f:
            html = f.read().decode('utf-8', errors='replace')
        # Find /api/asset?path=... image URLs
        for m in re.finditer(r'/api/asset\?path=([^"&\s]+)', html):
            raw = urllib.parse.unquote(m.group(1))
            if '/images/' in raw:
                basename = raw.split('/images/')[-1]
                all_images[raw] = basename

    # Download images
    for path, basename in all_images.items():
        url = f"https://pagefy.io/api/asset?path={urllib.parse.quote(path, safe='')}"
        dst = os.path.join(img_dir, basename)
        if not os.path.exists(dst):
            subprocess.run(['curl', '-sL', url, '--connect-timeout', '10', '-o', dst],
                         capture_output=True, timeout=15)
    print(f"Images: {len(all_images)} downloaded")

    # Copy all non-HTML resources
    for fn in os.listdir(html_dir):
        if fn.endswith('.html') or fn.startswith('.'): continue
        src = os.path.join(html_dir, fn)
        dst = os.path.join(output_dir, fn)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)

    # Process each chapter HTML
    base_path = None  # will be detected from the first link

    for slug, local_filename in slug_to_file.items():
        html_fn = f"{slug}.html"
        fpath = os.path.join(html_dir, html_fn)
        if not os.path.exists(fpath):
            print(f"  SKIP {html_fn}: not found")
            continue

        with open(fpath, 'rb') as f:
            html_bytes = f.read()
        html = html_bytes.decode('utf-8', errors='replace')

        # 1. Fix image paths (double-encoded by wget)
        def fix_img(m):
            raw = m.group(0)
            match = re.search(r'chap\d+-page\d+-img\d+\.png', raw, re.IGNORECASE)
            if match:
                return f'src="images/{match.group(0)}"'
            return raw
        html = re.sub(r'src="asset%3Fpath=[^"]+"', fix_img, html)

        # Also handle non-encoded versions
        def fix_img2(m):
            basename = m.group(1)
            return f'src="images/{basename}"'
        html = re.sub(r'src="[^"]*?/images/(chap\d+-page\d+-img\d+\.png)"', fix_img2, html)

        # 2. Replace text nodes
        replacements = []
        for m in re.finditer(r'>([^<]+)<', html):
            text = m.group(1)
            if text in lookup:
                trans = lookup[text]
                if trans != text:
                    replacements.append((m.start(1), m.end(1), trans))

        html_list = list(html)
        for start, end, trans in sorted(replacements, reverse=True):
            html_list[start:end] = trans
        html = ''.join(html_list)

        # 3. Fix internal chapter links
        for s, lf in slug_to_file.items():
            html = html.replace(f'href="/ai-engineering/ai-engineering-by-chip-huyen/{s}"', f'href="{lf}"')

        # 4. Fix _next/static paths to relative
        html = html.replace('/_next/static/', '_next/static/')

        # 5. Fix escaped quote artifacts
        html = html.replace('\\"', '"')

        # 6. Fix .js.1 etc suffixes
        html = re.sub(r'(\.(?:js|css|woff2|png|jpg|webp|svg|ico))\.1\b', r'\1', html)

        outname = local_filename
        outpath = os.path.join(output_dir, outname)
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(html)

        # Verify
        imgs = len(re.findall(r'src="images/', html))
        issues = []
        if re.findall(r'/api/asset', html): issues.append('API refs')
        if re.findall(r'"/_next/', html): issues.append('absolute _next')
        status = '✓' if not issues else '✗ ' + ','.join(issues)
        print(f"  {outname}: {len(replacements)} texts, {imgs} imgs {status}")

    # Summary
    htmls = [f for f in os.listdir(output_dir) if f.endswith('.html')]
    total = sum(os.path.getsize(os.path.join(output_dir, f)) for f in os.listdir(output_dir))
    print(f"\nDone: {len(htmls)} HTMLs, {len(os.listdir(output_dir))} files, {total/1024/1024:.1f} MB → {output_dir}/")

# ── Main ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Download HTML e-book, translate, make offline-ready')
    parser.add_argument('--base-url', required=True, help='Base URL of the book (e.g. https://example.com/book)')
    parser.add_argument('--slugs', nargs='+', required=True, help='Chapter URL slugs')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    parser.add_argument('--api', choices=['google', 'llm'], default='google', help='Translation backend (default: google)')
    parser.add_argument('--translation-file', help='Pre-translated file from LLM mode')
    parser.add_argument('--source-lang', default='en')
    parser.add_argument('--target-lang', default='zh-CN')
    parser.add_argument('--pagefy-images', action='store_true', help='Download images via pagefy /api/asset endpoint')
    args = parser.parse_args()

    base_url = args.base_url.rstrip('/')
    slugs = args.slugs
    output_dir = args.output

    # ── Generate slug → local filename mapping ──
    slug_to_file = {}
    for i, slug in enumerate(slugs):
        local_name = f"{i+1:02d}-{slug}-zh.html"
        slug_to_file[slug] = local_name

    work_dir = os.path.join(output_dir, '.work')
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Mirror
    print("=" * 60)
    print("Step 1: Mirroring chapters via wget...")
    mirror_chapters(base_url, slugs, work_dir)

    # Step 2: Extract texts
    print("\n" + "=" * 60)
    print("Step 2: Extracting text nodes...")
    texts = extract_texts(work_dir)
    print(f"  {len(texts)} unique translatable texts ({sum(len(t) for t in texts)} chars)")

    # Step 3: Translate
    print("\n" + "=" * 60)
    print("Step 3: Translating...")
    if args.translation_file:
        with open(args.translation_file) as f:
            translations = [line.rstrip('\n') for line in f if line.strip()]
    elif args.api == 'google':
        translations = translate_google(texts, args.source_lang, args.target_lang)
    else:
        translations = translate_llm(texts)

    # Step 4 & 5: Rebuild
    print("\n" + "=" * 60)
    print("Step 4-5: Rebuilding HTMLs...")
    rebuild(work_dir, output_dir, texts, translations, slug_to_file)

if __name__ == '__main__':
    main()
