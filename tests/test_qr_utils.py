import unittest
from qr_utils import generate_qr_code

class TestQRUtils(unittest.TestCase):
    def test_basic_qr(self):
        img = generate_qr_code("Hello World")
        self.assertIsNotNone(img)

    def test_custom_colors(self):
        img = generate_qr_code("Test", fill_color="red", back_color="yellow")
        self.assertIsNotNone(img)

if __name__ == "__main__":
    unittest.main()
