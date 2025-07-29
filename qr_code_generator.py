import os
import qrcode
from PIL import Image
from datetime import datetime
import argparse

def generate_qr_code(data, version=1, box_size=10, border=5, 
                    fill_color="black", back_color="white", 
                    logo_path=None):
    """
    Generates a QR code with the given parameters.
    
    Args:
        data: Data to encode
        version: QR code size (1-40)
        box_size: Size of each QR code "box"
        border: Border thickness
        fill_color: Module color
        back_color: Background color
        logo_path: Path to logo to embed in center (optional)
    
    Returns:
        PIL Image of generated QR code
    """
    qr = qrcode.QRCode(
        version=version,
        box_size=box_size,
        border=border,
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Add logo if specified
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo_size = min(img.size) // 4  # Logo size = 25% of QR code
        
        # Resize logo
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Position logo in center
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        
        # Create image with transparent background for logo
        logo_with_bg = Image.new("RGBA", img.size, (0, 0, 0, 0))
        logo_with_bg.paste(logo, pos)
        
        # Merge QR code and logo
        img = Image.alpha_composite(
            img.convert("RGBA"), 
            logo_with_bg
        )
    
    return img

def get_unique_filename(directory, base_name, extension):
    """
    Generates a unique filename with timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(directory, f"{base_name}_{timestamp}.{extension}")


if __name__ == '__main__':
    print("Veuillez utiliser l'interface graphique PyQt5 : python qr_code_gui_pyqt5.py")