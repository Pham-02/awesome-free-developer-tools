#!/usr/bin/env python3
"""Basic offline Markdown link inventory checker.

This script extracts HTTP(S) links from Markdown files and reports duplicates
and malformed-looking entries. It does not make network requests and cannot
verify whether a service is free. Use the GitHub Actions Lychee workflow for
online reachability checks.
"""
from pathlib import Path
import re
import sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = list(ROOT.rglob("*.md"))
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((https?://[^)\s]+)(?:\s+[^)]*)?\)")
URL_RE = re.compile(r"^https?://[^\s]+$")

links = []
issues = []

for path in MARKDOWN:
    if ".git" in path.parts:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    for match in LINK_RE.finditer(text):
        url = match.group(1).rstrip(".,;")
        line = text.count("\n", 0, match.start()) + 1
        links.append((url, path.relative_to(ROOT), line))
        if not URL_RE.match(url):
            issues.append(f"{path.relative_to(ROOT)}:{line}: suspicious URL: {url}")

counts = Counter(url for url, _, _ in links)
duplicates = {url: count for url, count in counts.items() if count > 1}

print(f"Scanned {len(MARKDOWN)} Markdown files.")
print(f"Found {len(links)} HTTP(S) Markdown links.")

if duplicates:
    print("\nRepeated URLs (may be intentional across categories):")
    for url, count in sorted(duplicates.items()):
        print(f"  {count}x {url}")

if issues:
    print("\nPotential formatting issues:")
    print("\n".join(issues))
    sys.exit(1)

print("\nOffline inventory complete. Run the GitHub Actions link check for network reachability.")
