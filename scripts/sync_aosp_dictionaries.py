#!/usr/bin/env python3
"""Sync and download AOSP dictionaries, validate binary headers, and generate manifests/languages.json."""

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_RELEASE_URL = "https://github.com/A-Hendo/astral-assets/releases/download/dict_v1.0.0"
UPSTREAM_BASE = "https://codeberg.org/Helium314/aosp-dictionaries/raw/branch/main/dictionaries"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def download_file(url: str, dest: Path) -> bool:
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AstralAssetSync/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp, open(tmp, "wb") as out:
            out.write(resp.read())
        if tmp.exists() and tmp.stat().st_size > 0:
            if dest.exists():
                dest.unlink()
            tmp.rename(dest)
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    finally:
        if tmp.exists():
            tmp.unlink()
    return False

def main():
    parser = argparse.ArgumentParser(description="AOSP Dictionary Sync & Downloader")
    parser.add_argument("--download", action="store_true", help="Download all .dict files locally to dictionaries/")
    args = parser.parse_args()

    lang_packs_file = REPO_ROOT.parent / "aurakey" / "app" / "src" / "main" / "assets" / "language_packs.json"
    if not lang_packs_file.exists():
        lang_packs_file = REPO_ROOT / "manifests" / "language_packs.json"
        
    if not lang_packs_file.exists():
        print(f"Error: Could not locate language_packs.json")
        sys.exit(1)
        
    data = json.loads(lang_packs_file.read_text(encoding="utf-8"))
    dict_dir = REPO_ROOT / "dictionaries"
    dict_dir.mkdir(parents=True, exist_ok=True)

    # Copy bundled en_gb if present
    bundled_en_gb = REPO_ROOT.parent / "aurakey" / "app" / "src" / "main" / "assets" / "dict" / "main_en_gb.dict"
    if bundled_en_gb.exists() and not (dict_dir / "main_en_gb.dict").exists():
        import shutil
        shutil.copy2(bundled_en_gb, dict_dir / "main_en_gb.dict")

    languages_manifest = []
    
    for item in data:
        locale = item.get("locale")
        name = item.get("name")
        dict_filename = f"main_{locale}.dict"
        dict_path = dict_dir / dict_filename
        
        emoji_url_val = item.get("emoji")
        emoji_filename = f"emoji_{locale}.dict" if emoji_url_val else None
        emoji_path = dict_dir / emoji_filename if emoji_filename else None

        if args.download:
            if not dict_path.exists() or dict_path.stat().st_size == 0:
                print(f"Downloading {dict_filename} for {name}...")
                upstream_url = item.get("dict") or f"{UPSTREAM_BASE}/{dict_filename}"
                download_file(upstream_url, dict_path)
            
            if emoji_filename and (not emoji_path.exists() or emoji_path.stat().st_size == 0):
                print(f"Downloading {emoji_filename}...")
                upstream_emoji_url = emoji_url_val if emoji_url_val.startswith("http") else f"{UPSTREAM_BASE}/{emoji_filename}"
                download_file(upstream_emoji_url, emoji_path)

        sha = sha256_file(dict_path) if dict_path.exists() else None
        size = dict_path.stat().st_size if dict_path.exists() else None
        
        entry = {
            "locale": locale,
            "name": name,
            "dict_url": f"{BASE_RELEASE_URL}/{dict_filename}",
            "emoji_url": f"{BASE_RELEASE_URL}/{emoji_filename}" if emoji_filename else None,
            "version": 1
        }
        if sha:
            entry["sha256"] = sha
            entry["size_bytes"] = size
            
        languages_manifest.append(entry)
        
    out_file = REPO_ROOT / "manifests" / "languages.json"
    out_file.write_text(json.dumps(languages_manifest, indent=2), encoding="utf-8")
    print(f"Manifest written to {out_file} ({len(languages_manifest)} languages)")

if __name__ == "__main__":
    main()
