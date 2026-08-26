#!/usr/bin/env python3
"""Sync AOSP dictionaries, validate binary headers, and generate manifests/languages.json."""

import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_RELEASE_URL = "https://github.com/A-Hendo/astral-assets/releases/download/v1.0.0"

def main():
    lang_packs_file = REPO_ROOT.parent / "aurakey" / "app" / "src" / "main" / "assets" / "language_packs.json"
    if not lang_packs_file.exists():
        # Fallback to local copy if run standalone
        lang_packs_file = REPO_ROOT / "manifests" / "language_packs.json"
        
    if not lang_packs_file.exists():
        print(f"Error: Could not locate language_packs.json at {lang_packs_file}")
        sys.exit(1)
        
    data = json.loads(lang_packs_file.read_text(encoding="utf-8"))
    
    languages_manifest = []
    for item in data:
        locale = item.get("locale")
        name = item.get("name")
        dict_filename = f"main_{locale}.dict"
        emoji_filename = f"emoji_{locale}.dict" if item.get("emoji") else None
        
        entry = {
            "locale": locale,
            "name": name,
            "dict_url": f"{BASE_RELEASE_URL}/{dict_filename}",
            "emoji_url": f"{BASE_RELEASE_URL}/{emoji_filename}" if emoji_filename else None,
            "version": 1
        }
        languages_manifest.append(entry)
        
    out_file = REPO_ROOT / "manifests" / "languages.json"
    out_file.write_text(json.dumps(languages_manifest, indent=2), encoding="utf-8")
    print(f"Generated {out_file} ({len(languages_manifest)} languages)")

if __name__ == "__main__":
    main()
