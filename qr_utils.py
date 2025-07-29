import os
import qrcode
from PIL import Image

def generate_qr_code(data, version=1, box_size=10, border=5,
                    fill_color="black", back_color="white",
                    logo_path=None):
    qr = qrcode.QRCode(
        version=version,
        box_size=box_size,
        border=border,
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo_size = min(img.size) // 4
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        logo_with_bg = Image.new("RGBA", img.size, (0, 0, 0, 0))
        logo_with_bg.paste(logo, pos)
        img = Image.alpha_composite(img.convert("RGBA"), logo_with_bg)
    return img
