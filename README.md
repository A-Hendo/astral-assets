# Astral Assets 🎨📦

This repository hosts official and community-contributed assets for [Astral Keyboard](https://github.com/A-Hendo/astral-keyboard), including themes, sound packs, dictionaries, neural models, fonts, and stickers.

---

## 📂 Repository Structure

```
astral-assets/
├── .github/
│   └── workflows/
│       ├── validate_community_assets.yml   # Automated PR validation
│       └── publish_release_assets.yml      # CI/CD manifest publishing
├── manifests/
│   ├── index.json                          # Root manifest linking all catalogs
│   ├── languages.json                      # 77 language dictionaries + emoji dicts
│   ├── themes.json                         # Official & community themes catalog
│   ├── sounds.json                         # Sound packs catalog
│   └── models.json                         # Neural TFLite language models
├── themes/
│   ├── official/                           # Official Astral themes (.akt)
│   ├── community/                          # Community-submitted themes (.akt)
│   └── previews/
│       ├── official/                       # WebP screenshots (~30KB) for official themes
│       └── community/                      # WebP screenshots for community themes
├── sounds/
│   ├── official/                           # Official sound packs (.zip)
│   └── community/                          # Community sound packs (.zip)
├── dictionaries/                           # AOSP binary dictionaries (.dict)
├── models/                                 # TFLite neural language models
├── fonts/                                  # Bundled typography TTF fonts
├── stickers/                               # Sticker packs & manifests
└── scripts/
    ├── validate_theme.py                   # Theme safety & schema validator
    ├── validate_sound.py                   # Sound pack validator
    ├── generate_manifests.py               # Manifest generator (SHA-256 + metadata)
    └── sync_aosp_dictionaries.py           # AOSP dictionary sync utility
```

---

## 🚀 Distribution Model

* **Metadata & Previews (GitHub Raw CDN):** Dynamic manifests (`manifests/*.json`) and lightweight WebP preview screenshots are served via `raw.githubusercontent.com` from `main` for instant catalog updates without requiring app updates.
* **Heavy Binary Assets (GitHub Releases):** Binary blobs (`.dict`, `.tflite`, `.akt`, `.zip`, `.ttf`) are hosted via GitHub Releases (`objects.githubusercontent.com`), supporting resumable chunked downloads and preventing Git repository bloat.

---

## 🎨 Contributing Themes & Sound Packs

We welcome community contributions!

### Submitting a Theme (`.akt`)
1. Create a theme using Astral Keyboard’s in-app Theme Builder or author an `.akt` package manually.
2. Fork this repository.
3. Place your `.akt` file in `themes/community/<theme_id>.akt`.
4. Include a companion WebP preview screenshot (under 200 KB) in `themes/previews/community/<theme_id>_preview.webp`.
5. Run the local validator:
   ```bash
   python3 scripts/validate_theme.py themes/community/<theme_id>.akt
   ```
6. Open a Pull Request.

### Submitting a Sound Pack (`.zip`)
1. Package your sound effects into a `.zip` archive containing `.wav`, `.mp3`, or `.ogg` files (total pack size $\le$ 5 MB).
2. Place your archive in `sounds/community/<pack_id>.zip`.
3. Run the sound validator:
   ```bash
   python3 scripts/validate_sound.py sounds/community/<pack_id>.zip
   ```
4. Open a Pull Request.

---

## 📜 License
Assets and code in this repository are licensed under the [Apache 2.0 License](LICENSE).
