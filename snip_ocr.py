import os
import shutil
import sys
import tempfile
import urllib.request

import pytesseract
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import ImageGrab


class SnipOverlay(QtWidgets.QWidget):
    """Fullscreen translucent overlay that lets the user drag a rectangle and captures it."""

    def __init__(self, on_complete, tesseract_cmd=None):
        super().__init__()
        self.on_complete = on_complete
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setWindowOpacity(0.3)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.start = None
        self.end = None
        self.pen = QtGui.QPen(QtGui.QColor(0, 120, 215), 2, QtCore.Qt.SolidLine)

    def paintEvent(self, event):
        if self.start and self.end:
            qp = QtGui.QPainter(self)
            qp.setPen(self.pen)
            rect = QtCore.QRect(self.start, self.end)
            qp.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.capture_and_ocr()
        self.close()

    def capture_and_ocr(self):
        if not (self.start and self.end):
            return
        rect = QtCore.QRect(self.start, self.end).normalized()
        geometry = QtWidgets.QApplication.primaryScreen().geometry()
        x1 = geometry.x() + rect.left()
        y1 = geometry.y() + rect.top()
        x2 = geometry.x() + rect.right()
        y2 = geometry.y() + rect.bottom()
        bbox = (x1, y1, x2, y2)
        img = ImageGrab.grab(bbox)
        text = pytesseract.image_to_string(img)
        self.on_complete(text, img)


class MainWindow(QtWidgets.QWidget):
    """Small toolbar-style window similar to Snipping Tool."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snip to Text")
        self.setFixedWidth(520)
        self.last_text = ""
        self.tesseract_path = ""

        self.build_ui()
        self.ensure_tesseract_ready()

    def build_ui(self):
        # Top toolbar row
        toolbar = QtWidgets.QHBoxLayout()
        toolbar.setSpacing(8)

        title = QtWidgets.QLabel("Snip to Text")
        title.setStyleSheet("font-weight: 600;")

        self.new_btn = QtWidgets.QPushButton("New")
        self.new_btn.setStyleSheet("background:#1890ff;color:white;padding:6px 12px;")
        self.new_btn.clicked.connect(self.start_snip)

        self.mode_label = QtWidgets.QLabel("Mode:")
        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItems(["Rectangular"])
        self.mode_combo.setEnabled(False)  # only rectangular supported for now

        self.delay_label = QtWidgets.QLabel("Delay (s):")
        self.delay_spin = QtWidgets.QSpinBox()
        self.delay_spin.setRange(0, 10)
        self.delay_spin.setValue(0)

        self.options_btn = QtWidgets.QPushButton("Options")
        self.options_btn.clicked.connect(self.pick_tesseract)

        self.copy_btn = QtWidgets.QPushButton("Copy Text")
        self.copy_btn.clicked.connect(self.copy_text)

        toolbar.addWidget(title)
        toolbar.addStretch(1)
        toolbar.addWidget(self.new_btn)
        toolbar.addWidget(self.mode_label)
        toolbar.addWidget(self.mode_combo)
        toolbar.addWidget(self.delay_label)
        toolbar.addWidget(self.delay_spin)
        toolbar.addWidget(self.options_btn)
        toolbar.addWidget(self.copy_btn)

        # Text output area
        self.text_area = QtWidgets.QTextEdit()
        self.text_area.setPlaceholderText("Captured text will appear here...")
        self.text_area.setMinimumHeight(140)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(toolbar)
        layout.addWidget(self.text_area)
        self.setLayout(layout)

    def start_snip(self):
        self.hide()
        delay_ms = self.delay_spin.value() * 1000
        QtCore.QTimer.singleShot(delay_ms, self.launch_overlay)

    def launch_overlay(self):
        self.overlay = SnipOverlay(
            on_complete=self.handle_snip_done, tesseract_cmd=self.tesseract_path or None
        )
        self.overlay.show()

    def handle_snip_done(self, text, img):
        self.last_text = text or ""
        self.text_area.setPlainText(self.last_text if self.last_text.strip() else "(no text found)")
        QtWidgets.QApplication.clipboard().setText(self.last_text)
        self.showNormal()
        self.activateWindow()

    def copy_text(self):
        QtWidgets.QApplication.clipboard().setText(self.text_area.toPlainText())

    def pick_tesseract(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select tesseract.exe", "", "Executables (*.exe)"
        )
        if path:
            self.tesseract_path = path
            QtWidgets.QMessageBox.information(self, "Tesseract set", f"Using:\n{path}")

    # --- Tesseract handling -------------------------------------------------
    def locate_tesseract_path(self):
        """Try to find a usable tesseract executable."""
        if self.tesseract_path and os.path.exists(self.tesseract_path):
            return self.tesseract_path
        found = shutil.which("tesseract")
        if found:
            return found
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for candidate in common_paths:
            if os.path.exists(candidate):
                return candidate
        return None

    def ensure_tesseract_ready(self):
        """Check for tesseract; if missing, prompt to select or download."""
        path = self.locate_tesseract_path()
        if path:
            self.tesseract_path = path
            return

        while not path:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Tesseract not found")
            msg.setText("Tesseract OCR is not installed or not on PATH.")
            select_btn = msg.addButton("Select tesseract.exe", QtWidgets.QMessageBox.ActionRole)
            download_btn = msg.addButton("Download and install", QtWidgets.QMessageBox.ActionRole)
            cancel_btn = msg.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)
            msg.exec_()

            clicked = msg.clickedButton()
            if clicked == select_btn:
                self.pick_tesseract()
                path = self.locate_tesseract_path()
            elif clicked == download_btn:
                if self.download_tesseract():
                    # After installer, try to locate again.
                    path = self.locate_tesseract_path()
                else:
                    path = None
            else:
                break

        if path:
            self.tesseract_path = path
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Tesseract missing",
                "Tesseract is still not available. Please install or select it before capturing.",
            )

    def download_tesseract(self):
        """Download the Windows installer and launch it."""
        url = (
            "https://github.com/UB-Mannheim/tesseract/releases/download/"
            "v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe"
        )
        try:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
            tmp_path = tmp.name
            tmp.close()
            progress = QtWidgets.QProgressDialog(
                "Downloading Tesseract installer...", "Cancel", 0, 100, self
            )
            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setAutoClose(True)
            progress.setValue(0)

            def report(block_num, block_size, total_size):
                if progress.wasCanceled():
                    raise Exception("Download cancelled by user")
                if total_size > 0:
                    percent = int(block_num * block_size * 100 / total_size)
                    progress.setValue(min(percent, 100))
                QtWidgets.QApplication.processEvents()

            urllib.request.urlretrieve(url, tmp_path, reporthook=report)
            progress.setValue(100)
            os.startfile(tmp_path)  # Launch installer
            QtWidgets.QMessageBox.information(
                self,
                "Installer launched",
                "Complete the installer, then click OK to re-check for Tesseract.",
            )
            return True
        except Exception as exc:  # pylint: disable=broad-except
            QtWidgets.QMessageBox.critical(
                self,
                "Download failed",
                f"Could not download Tesseract automatically.\nError: {exc}",
            )
            return False


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()