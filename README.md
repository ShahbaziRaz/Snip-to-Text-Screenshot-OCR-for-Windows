# Snip to Text – Screenshot OCR for Windows

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-red.svg)

**⚡ Lightweight OCR tool to instantly convert any screen region into editable text**

</div>

---

## 📸 Overview

Drag a region on your screen and instantly convert it to editable text using Tesseract OCR. Perfect for copying text from images, PDFs, locked documents, or videos—no more retyping!

## ✨ Features

- 🎯 **One-Click Snipping**: Instant overlay with rectangular selection
- 📋 **Clipboard-First**: Recognized text auto-copied to clipboard
- ⏱️ **Delay Timer**: Optional countdown to prepare your screen
- 🛠️ **Tesseract Helper**: Auto-detect existing install or download the engine for you

## 📋 Requirements

- **OS**: Windows 10 / 11
- **Python**: 3.9 or higher
- **Tesseract OCR**: Auto-detected or downloaded via the app

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/ShahbaziRaz/Snip-to-Text-Screenshot-OCR-for-Windows

# 2. Navigate to project folder
cd snip-to-text

# 3. Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Launch the application
python snip_ocr.py
```

Click **New**, drag to select any area, and your OCR text appears instantly—already copied to clipboard!

## 📦 Packaging (Optional)

Create a standalone `.exe` with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name "Snip to Text" snip_ocr.py
```

The executable will be in the `dist/` folder.

## 📁 Project Structure

```
snip-to-text/
├── snip_ocr.py          # Main PyQt5 application
├── requirements.txt     # Python dependencies
├── LICENSE             # MIT license
└── README.md
```

## 🔍 Keywords

Windows OCR, screenshot text extraction, Python OCR app, PyQt5 snipping tool, Tesseract GUI, screen capture OCR, image to text converter

---

<div align="center">

⭐ **Enjoying Snip to Text?** Don't forget to star the repository!

</div>
