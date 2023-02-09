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
    data = input("Enter the data to be encoded in QR Code: ")
    img = generate_qr_code(data)
    img.show()
