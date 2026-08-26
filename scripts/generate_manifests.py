#!/usr/bin/env python3
"""Generate catalog manifests (index.json, themes.json, sounds.json, models.json) for Astral Keyboard assets."""

import hashlib
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_RAW_URL = "https://raw.githubusercontent.com/A-Hendo/astral-assets/main"
BASE_THEMES_RELEASE_URL = "https://github.com/A-Hendo/astral-assets/releases/download/themes_v1.0.0"
BASE_SOUNDS_RELEASE_URL = "https://github.com/A-Hendo/astral-assets/releases/download/sounds_v1.0.0"
BASE_MODELS_RELEASE_URL = "https://github.com/A-Hendo/astral-assets/releases/download/models_v1.0.0" 

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def generate_themes_manifest():
    themes = []
    themes_dir = REPO_ROOT / "themes"
    
    for category in ["official", "community"]:
        cat_dir = themes_dir / category
        if not cat_dir.exists():
            continue
            
        for akt_file in sorted(cat_dir.glob("*.akt")):
            theme_id = akt_file.stem
            size_bytes = akt_file.stat().st_size
            sha = sha256_file(akt_file)
            
            # Read name from JSON if plain json
            theme_name = theme_id.replace("_", " ").title()
            try:
                content = akt_file.read_bytes()
                if not content.startswith(b"PK\x03\x04"):
                    data = json.loads(content.decode("utf-8"))
                    theme_name = data.get("name", theme_name)
            except Exception:
                pass
                
            preview_filename = f"{theme_id}_preview.webp"
            preview_path = themes_dir / "previews" / category / preview_filename
            
            entry = {
                "id": theme_id,
                "name": theme_name,
                "category": category,
                "author": "Astral Team" if category == "official" else "Community",
                "author_url": "https://github.com/A-Hendo" if category == "official" else "",
                "version": 1,
                "download_url": f"{BASE_THEMES_RELEASE_URL}/{akt_file.name}",
                "preview_url": f"{BASE_RAW_URL}/themes/previews/{category}/{preview_filename}" if preview_path.exists() else None,
                "sha256": sha,
                "size_bytes": size_bytes
            }
            themes.append(entry)
            
    out_path = REPO_ROOT / "manifests" / "themes.json"
    out_path.write_text(json.dumps(themes, indent=2), encoding="utf-8")
    print(f"Generated {out_path} ({len(themes)} themes)")

def generate_sounds_manifest():
    sounds = []
    sounds_dir = REPO_ROOT / "sounds"
    audio_extensions = {".wav", ".mp3", ".ogg"}
    
    for category in ["official", "community"]:
        cat_dir = sounds_dir / category
        if not cat_dir.exists():
            continue
            
        for audio_file in sorted(cat_dir.glob("*")):
            if audio_file.suffix.lower() not in audio_extensions or not audio_file.is_file():
                continue
                
            sound_id = audio_file.stem
            size_bytes = audio_file.stat().st_size
            sha = sha256_file(audio_file)
            
            entry = {
                "id": sound_id,
                "name": sound_id.replace("_", " ").title(),
                "filename": audio_file.name,
                "category": category,
                "author": "Astral Team" if category == "official" else "Community",
                "version": 1,
                "download_url": f"{BASE_SOUNDS_RELEASE_URL}/{audio_file.name}",
                "sha256": sha,
                "size_bytes": size_bytes
            }
            sounds.append(entry)
            
    out_path = REPO_ROOT / "manifests" / "sounds.json"
    out_path.write_text(json.dumps(sounds, indent=2), encoding="utf-8")
    print(f"Generated {out_path} ({len(sounds)} sounds)")

def generate_index_manifest():
    index = {
        "version": 1,
        "languages": f"{BASE_RAW_URL}/manifests/languages.json",
        "themes": f"{BASE_RAW_URL}/manifests/themes.json",
        "sounds": f"{BASE_RAW_URL}/manifests/sounds.json",
        "models": f"{BASE_RAW_URL}/manifests/models.json"
    }
    out_path = REPO_ROOT / "manifests" / "index.json"
    out_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Generated {out_path}")

def generate_models_manifest():
    models = {
        "version": 1,
        "base_url": BASE_MODELS_RELEASE_URL,
        "bundled_locales": ["en"],
        "cloud_locales": [
            "ar", "cs", "da", "de", "el", "es", "fi", "fr", "hu", "id", "it",
            "nl", "no", "pl", "pt", "ro", "ru", "sk", "sv", "tr", "uk"
        ]
    }
    out_path = REPO_ROOT / "manifests" / "models.json"
    out_path.write_text(json.dumps(models, indent=2), encoding="utf-8")
    print(f"Generated {out_path}")

def main():
    REPO_ROOT.joinpath("manifests").mkdir(parents=True, exist_ok=True)
    generate_themes_manifest()
    generate_sounds_manifest()
    generate_models_manifest()
    generate_index_manifest()

if __name__ == "__main__":
    main()
