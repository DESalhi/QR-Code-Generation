import sys
import os
from qr_utils import generate_qr_code
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
    QColorDialog, QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QGroupBox, QStatusBar
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

## QR code generation logic is now in qr_utils.py

def pil2pixmap(im):
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    data = im.tobytes("raw", "RGBA")
    qimg = QImage(data, im.size[0], im.size[1], QImage.Format_RGBA8888)
    return QPixmap.fromImage(qimg)

from PyQt5.QtWidgets import QGroupBox, QStatusBar

class QRCodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator (PyQt5)")
        self.setGeometry(100, 100, 520, 480)
        self.qr_img = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Styled title
        title = QLabel("QR Code Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:28px; color:#2196F3; font-weight:bold; margin-bottom:10px;")
        main_layout.addWidget(title)

        # GroupBox: Data and logo (horizontal)
        input_group = QGroupBox("Informations")
        input_layout = QHBoxLayout()

        # Data
        data_layout = QVBoxLayout()
        data_label = QLabel("Data to encode:")
        self.data_edit = QLineEdit()
        self.data_edit.setPlaceholderText("Data to encode")
        data_layout.addWidget(data_label)
        data_layout.addWidget(self.data_edit)

        # Logo
        logo_layout = QVBoxLayout()
        logo_label = QLabel("Logo (optional):")
        logo_hlayout = QHBoxLayout()
        self.logo_edit = QLineEdit()
        self.logo_edit.setPlaceholderText("Logo path (optional)")
        logo_btn = QPushButton("Browse")
        logo_btn.clicked.connect(self.choose_logo)
        logo_btn.setStyleSheet("border-radius:8px; background:#E3F2FD; padding:4px 12px; font-weight:bold;")
        logo_hlayout.addWidget(self.logo_edit)
        logo_hlayout.addWidget(logo_btn)
        logo_layout.addWidget(logo_label)
        logo_layout.addLayout(logo_hlayout)

        # Add both sections side by side
        input_layout.addLayout(data_layout)
        input_layout.addLayout(logo_layout)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # GroupBox: Colors
        color_group = QGroupBox("Personnalisation")
        color_layout = QHBoxLayout()
        self.fill_color = "black"
        self.back_color = "white"
        fill_btn = QPushButton("Choose Fill Color")
        fill_btn.clicked.connect(self.choose_fill_color)
        fill_btn.setStyleSheet("border-radius:8px; background:#BBDEFB; padding:4px 12px; font-weight:bold;")
        back_btn = QPushButton("Choose Background Color")
        back_btn.clicked.connect(self.choose_back_color)
        back_btn.setStyleSheet("border-radius:8px; background:#BBDEFB; padding:4px 12px; font-weight:bold;")
        color_layout.addWidget(QLabel("Fill Color:"))
        color_layout.addWidget(fill_btn)
        color_layout.addWidget(QLabel("Background Color:"))
        color_layout.addWidget(back_btn)
        color_group.setLayout(color_layout)
        main_layout.addWidget(color_group)

        # Action buttons
        btn_layout = QHBoxLayout()
        gen_btn = QPushButton("Generate QR Code")
        gen_btn.clicked.connect(self.generate)
        gen_btn.setStyleSheet("border-radius:12px; background:#4CAF50; color:white; font-weight:bold; padding:8px 18px;")
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_form)
        reset_btn.setStyleSheet("border-radius:12px; background:#FFC107; color:black; font-weight:bold; padding:8px 18px;")
        btn_layout.addWidget(gen_btn)
        btn_layout.addWidget(reset_btn)
        main_layout.addLayout(btn_layout)

        # QR code preview
        preview_group = QGroupBox("Aperçu")
        preview_layout = QVBoxLayout()
        self.img_label = QLabel()
        self.img_label.setFrameShape(QFrame.Box)
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setMinimumSize(220, 220)
        preview_layout.addWidget(self.img_label)
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)

        # Save button
        save_btn = QPushButton("Save QR Code")
        save_btn.clicked.connect(self.save)
        save_btn.setStyleSheet("border-radius:12px; background:#2196F3; color:white; font-weight:bold; padding:8px 18px;")
        main_layout.addWidget(save_btn)

        # (Batch CSV button removed)
    # (batch_generate method removed)

        # Status bar
        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)

    def reset_form(self):
        self.data_edit.clear()
        self.logo_edit.clear()
        self.fill_color = "black"
        self.back_color = "white"
        self.img_label.clear()
        self.status_bar.showMessage("Form reset.", 2000)

    def choose_logo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.logo_edit.setText(path)

    def choose_fill_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_color = color.name()

    def choose_back_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.back_color = color.name()

    def generate(self):
        data = self.data_edit.text()
        logo = self.logo_edit.text() if self.logo_edit.text() and os.path.exists(self.logo_edit.text()) else None
        if not data:
            QMessageBox.critical(self, "Error", "Data cannot be empty.")
            self.status_bar.showMessage("Erreur : données manquantes", 3000)
            return
        try:
            self.qr_img = generate_qr_code(data=data, fill_color=self.fill_color, back_color=self.back_color, logo_path=logo)
            pixmap = pil2pixmap(self.qr_img.resize((220, 220)))
            self.img_label.setPixmap(pixmap)
            self.status_bar.showMessage("QR code généré avec succès", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_bar.showMessage(f"Erreur : {str(e)}", 3000)

    def save(self):
        if self.qr_img is None:
            QMessageBox.critical(self, "Error", "No QR code to save.")
            self.status_bar.showMessage("Erreur : aucun QR code à sauvegarder", 3000)
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save QR Code",
            "qrcode.png",
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;SVG Image (*.svg)"
        )
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()
            try:
                if ext == ".svg":
                    # Export SVG
                    import qrcode
                    from qrcode.image.svg import SvgImage
                    # Re-generate QR code as SVG
                    qr = qrcode.QRCode(
                        version=1,
                        box_size=10,
                        border=5,
                        error_correction=qrcode.constants.ERROR_CORRECT_H
                    )
                    qr.add_data(self.data_edit.text())
                    qr.make(fit=True)
                    img_svg = qr.make_image(image_factory=SvgImage)
                    img_svg.save(file_path)
                else:
                    # PNG/JPEG
                    self.qr_img.save(file_path)
                QMessageBox.information(self, "Saved", f"Image saved successfully: {file_path}")
                self.status_bar.showMessage("Image sauvegardée", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Save failed: {str(e)}")
                self.status_bar.showMessage(f"Erreur sauvegarde : {str(e)}", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeApp()
    window.show()
    sys.exit(app.exec_())
