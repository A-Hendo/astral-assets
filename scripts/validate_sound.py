#!/usr/bin/env python3
"""Sound pack validator for Astral Keyboard .zip sound packs."""

import os
import sys
import zipfile
from pathlib import Path

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg"}
MAX_PACK_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

def validate_sound_pack(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        print(f"Error: File not found: {path}")
        return False
        
    size = path.stat().st_size
    if size > MAX_PACK_SIZE_BYTES:
        print(f"Error [{path.name}]: Pack size exceeds 5 MB ({size / (1024*1024):.2f} MB)")
        return False
        
    try:
        with zipfile.ZipFile(path, "r") as zf:
            infolist = zf.infolist()
            if not infolist:
                print(f"Error [{path.name}]: Empty zip archive")
                return False
                
            audio_count = 0
            for entry in infolist:
                name = entry.filename
                if ".." in name or name.startswith("/") or name.startswith("\\"):
                    print(f"Error [{path.name}]: Dangerous path traversal in zip entry: {name}")
                    return False
                ext = Path(name).suffix.lower()
                if ext in ALLOWED_EXTENSIONS:
                    audio_count += 1
                elif ext and ext != ".txt" and ext != ".json":
                    print(f"Warning [{path.name}]: Non-audio file present: {name}")
                    
            if audio_count == 0:
                print(f"Error [{path.name}]: No valid audio files (.wav, .mp3, .ogg) found in pack")
                return False
                
    except Exception as e:
        print(f"Error [{path.name}]: Invalid or corrupted zip ({e})")
        return False
        
    print(f"OK: {path.name} ({audio_count} audio files, {size / 1024:.1f} KB)")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_sound.py <path_to_zip_or_dir>")
        sys.exit(1)
        
    target = Path(sys.argv[1])
    files = [target] if target.is_file() else sorted(list(target.glob("**/*.zip")))
    
    if not files:
        print(f"No sound pack .zip files found in {target}")
        sys.exit(0)
        
    all_ok = True
    for f in files:
        if not validate_sound_pack(f):
            all_ok = False
            
    if not all_ok:
        sys.exit(1)
    print(f"All {len(files)} sound pack(s) passed validation!")

if __name__ == "__main__":
    main()
