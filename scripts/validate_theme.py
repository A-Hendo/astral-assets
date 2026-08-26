#!/usr/bin/env python3
"""Theme validator for Astral Keyboard .akt files."""

import json
import os
import sys
import zipfile
from pathlib import Path

REQUIRED_COLOR_KEYS = {
    "keyboardBackground",
    "toolbarBackground",
    "keyBackground",
    "keyBorder",
    "keyText",
    "keySubText",
    "accentColor",
    "accentBg",
    "popupBackground",
}

MAX_AGSL_LENGTH = 8192

def validate_theme_json(data: dict, filename: str) -> bool:
    name = data.get("name")
    if not name:
        print(f"Error [{filename}]: Missing top-level name field")
        return False
    
    colors = data.get("colors")
    if not isinstance(colors, dict):
        print(f"Error [{filename}]: Missing or invalid colors object")
        return False
    
    missing_colors = REQUIRED_COLOR_KEYS - set(colors.keys())
    if missing_colors:
        print(f"Error [{filename}]: Missing required color keys: {missing_colors}")
        return False
    
    shaders = data.get("shaders", {})
    if isinstance(shaders, dict):
        for block_name, block in shaders.items():
            if isinstance(block, dict) and block.get("type") == "CUSTOM":
                src = block.get("source", "")
                if len(src) > MAX_AGSL_LENGTH:
                    print(f"Error [{filename}]: Custom shader {block_name} exceeds {MAX_AGSL_LENGTH} chars ({len(src)})")
                    return False
    return True

def validate_akt_file(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        print(f"Error: File does not exist: {path}")
        return False
    
    content = path.read_bytes()
    if content.startswith(b"PK\x03\x04"):
        try:
            with zipfile.ZipFile(path, "r") as zf:
                theme_json_found = False
                for entry in zf.infolist():
                    name = entry.filename
                    if ".." in name or name.startswith("/") or name.startswith("\\"):
                        print(f"Error [{path.name}]: Zip entry contains path traversal: {name}")
                        return False
                    if name.endswith(".akt") and not theme_json_found:
                        theme_data = json.loads(zf.read(name).decode("utf-8"))
                        if not validate_theme_json(theme_data, f"{path.name}:{name}"):
                            return False
                        theme_json_found = True
                if not theme_json_found:
                    print(f"Error [{path.name}]: Zip package does not contain an inner .akt JSON file")
                    return False
        except Exception as e:
            print(f"Error [{path.name}]: Corrupted zip package ({e})")
            return False
    else:
        try:
            theme_data = json.loads(content.decode("utf-8"))
            if not validate_theme_json(theme_data, path.name):
                return False
        except Exception as e:
            print(f"Error [{path.name}]: Invalid JSON format ({e})")
            return False
            
    print(f"OK: {path.name}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_theme.py <path_to_akt_file_or_dir>")
        sys.exit(1)
        
    target = Path(sys.argv[1])
    files = [target] if target.is_file() else sorted(list(target.glob("**/*.akt")))
    
    if not files:
        print(f"No .akt files found in {target}")
        sys.exit(0)
        
    all_ok = True
    for f in files:
        if not validate_akt_file(f):
            all_ok = False
            
    if not all_ok:
        sys.exit(1)
    print(f"All {len(files)} theme(s) passed validation!")

if __name__ == "__main__":
    main()
