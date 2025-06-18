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

def main():
    try:
        # Configure command line arguments
        parser = argparse.ArgumentParser(description='QR Code Generator')
        parser.add_argument('--data', type=str, help='Data to encode')
        parser.add_argument('--output', type=str, help='Output path')
        parser.add_argument('--logo', type=str, help='Logo to embed')
        args = parser.parse_args()

        # Get data if not provided as argument
        data = args.data if args.data else input("Enter data to encode in QR Code: ")
        if not data:
            raise ValueError("Data cannot be empty.")

        # Get logo if not provided as argument
        logo_path = args.logo
        if not logo_path and input("Add a logo? (y/n): ").lower() == 'y':
            logo_path = input("Enter logo path: ")

        # Generate QR code
        img = generate_qr_code(
            data=data,
            logo_path=logo_path if logo_path and os.path.exists(logo_path) else None
        )
        
        # Display image
        img.show()

        # Save image
        save_option = 'y' if args.output else input("Save QR Code? (y/n): ")
        if save_option.lower() == 'y':
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Use provided path or generate unique name
            if args.output:
                file_path = args.output
            else:
                file_path = get_unique_filename(script_dir, "qrcode", "png")
            
            img.save(file_path)
            print(f"Image saved successfully: {file_path}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()