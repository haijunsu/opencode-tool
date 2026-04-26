# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`opencode-tool` is a Python utility suite with two independent CLI tools: an ASCII art generator and a passport/visa photo generator. Tools run directly from source via bash wrapper scripts — there is no build step or package installation.

## Commands

**Run tests:**
```bash
pytest                    # all tests
pytest tests/unit/test_ascii_art.py        # single test file
pytest tests/unit/test_ascii_art.py::test_name  # single test
```

**Lint and type-check:**
```bash
flake8 src/
mypy src/
pylint src/
```

**Run tools directly:**
```bash
python3 scripts/ascii_art "Hello World"
python3 scripts/passport_photo input.jpg output.jpg --type cn_passport --color blue --layout
```

**Install dependencies:**
```bash
pip install -r requirements.txt       # production
pip install -r requirements-dev.txt   # dev/test tools
```

## Architecture

Each tool is self-contained in `src/opencode_tool/` with a corresponding bash wrapper in `scripts/` and tests in `tests/unit/`.

**`ascii_art.py`** — Pure Python, no external deps. A hardcoded `FONT` dict maps characters (a–z, 0–9, space, hyphen) to 7-row bitmaps. `ascii_art(text)` converts each char to its bitmap rows, normalizes widths, and joins them side-by-side.

**`passport_photo.py`** — Uses `rembg`, `opencv-python`, `numpy`, and `Pillow`. The core pipeline: remove background with `rembg` → detect face with OpenCV Haar cascade → calculate crop/resize ratios relative to face width → paste onto solid-color background. Photo specs live in `PHOTO_PROFILES` (a dict of `ProfileDict` TypedDicts). The `--layout` flag tiles multiple photos onto a 4×6 inch / 300 DPI print sheet with black dividing lines.

**Optional dependency pattern:** Both modules import heavy libraries with a `cast(None, ...)` fallback so imports never hard-fail; `check_dependencies()` gates actual usage at runtime.

## Photo Profiles

Defined in `PHOTO_PROFILES` in `passport_photo.py`:
- `cn_passport` — 390×567 px (33×48 mm), default blue background
- `us_passport` — 600×600 px (2×2 in), white background only
- `us_visa` — 600×600 px (2×2 in), white background only

To add a new profile, add an entry to `PHOTO_PROFILES` with keys: `width`, `height`, `face_ratio`, `face_top_ratio`, `dpi`, `bg_color`.

## Key Conventions

- Entry points for both tools are `main()` functions called under `if __name__ == "__main__"`.
- The ASCII art font is stored as a plain dict — extending it means adding a 7-element list of strings per new character.
- No `__init__.py` exists under `src/opencode_tool/` — modules are not installed as a package.
- There is no `pyproject.toml` or `setup.py`; dependency management is manual via `requirements*.txt`.
