# Snip to Text – Screenshot OCR for Windows

Lightweight PyQt5 app that lets you drag a region on screen and instantly convert it to editable text using Tesseract OCR. Great for copying text from images, PDFs, locked documents, or videos without retyping.

## Features

- One-click "New" snip overlay with rectangular selection.
- Clipboard-first workflow: recognized text is auto-copied.
- Optional delay timer to prep the screen before capture.
- Built-in Tesseract helper: locate existing install or download the Windows installer for you.

## Requirements

- Windows 10/11.
- Python 3.9+.
- Tesseract OCR (auto-detected; you can browse to `tesseract.exe` or download from the app prompt).

## Quick Start

1. Clone the repo:
   ```bash
   git clone https://github.com/ShahbaziRaz/Snip-to-Text-Screenshot-OCR-for-Windows
   cd snip-to-text
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python snip_ocr.py
   ```
5. Click **New**, drag to select the area, and your OCR text appears and is copied automatically.

## Packaging (optional)

You can create a standalone Windows executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name "Snip to Text" snip_ocr.py
```

The binary will be in `dist/`.

## Project Structure

- `snip_ocr.py` — main PyQt5 application and overlay logic.
- `requirements.txt` — Python dependencies.
- `LICENSE` — MIT license.

## SEO keywords

Windows OCR screenshot tool, Python OCR app, PyQt snipping tool, convert image to text, Tesseract Windows GUI, copy text from screenshot, screen capture OCR.
