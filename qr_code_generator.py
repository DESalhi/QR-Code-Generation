import os
import qrcode
from PIL import Image

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    return img


if __name__ == '__main__':
    try:
        data = input("Enter the data to be encoded in QR Code: ")
        if not data:
            raise ValueError("Data cannot be empty.")

        img = generate_qr_code(data)
        img.show()

        save_option = input("Do you want to save the QR Code image? (y/n): ")
        if save_option.lower() == 'y':
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "qrcode.png")
            img.save(file_path)
            print("Image saved successfully.")
    except Exception as e:
        print("An error occurred:", str(e))
