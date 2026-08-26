#!/usr/bin/env python3
"""Audio sound file validator for Astral Keyboard (.wav, .mp3, .ogg)."""

import os
import sys
from pathlib import Path

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg"}
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB

def validate_sound_file(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        print(f"Error: File not found: {path}")
        return False
        
    ext = path.suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        print(f"Error [{path.name}]: Unsupported audio extension {ext} (must be .wav, .mp3, or .ogg)")
        return False
        
    size = path.stat().st_size
    if size > MAX_FILE_SIZE_BYTES:
        print(f"Error [{path.name}]: File size exceeds 2 MB ({size / 1024:.1f} KB)")
        return False
        
    if size < 64:
        print(f"Error [{path.name}]: File appears empty or corrupted ({size} bytes)")
        return False
        
    print(f"OK: {path.name} ({size / 1024:.1f} KB)")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_sound.py <path_to_audio_or_dir>")
        sys.exit(1)
        
    target = Path(sys.argv[1])
    if target.is_file():
        files = [target]
    else:
        files = [f for f in sorted(target.glob("**/*")) if f.suffix.lower() in ALLOWED_EXTENSIONS and f.is_file()]
    
    if not files:
        print(f"No audio files (.wav, .mp3, .ogg) found in {target}")
        sys.exit(0)
        
    all_ok = True
    for f in files:
        if not validate_sound_file(f):
            all_ok = False
            
    if not all_ok:
        sys.exit(1)
    print(f"All {len(files)} sound file(s) passed validation!")

if __name__ == "__main__":
    main()
