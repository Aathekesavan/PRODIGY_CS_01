import unittest
from caesar_cipher import CaesarCipher

class TestCaesarCipher(unittest.TestCase):
    
    def test_encrypt_standard(self):
        # Basic lowercase and uppercase
        self.assertEqual(CaesarCipher.encrypt("abc", 3), "def")
        self.assertEqual(CaesarCipher.encrypt("xyz", 3), "abc")
        self.assertEqual(CaesarCipher.encrypt("ABC", 3), "DEF")
        self.assertEqual(CaesarCipher.encrypt("XYZ", 3), "ABC")

    def test_decrypt_standard(self):
        self.assertEqual(CaesarCipher.decrypt("def", 3), "abc")
        self.assertEqual(CaesarCipher.decrypt("abc", 3), "xyz")
        self.assertEqual(CaesarCipher.decrypt("DEF", 3), "ABC")
        self.assertEqual(CaesarCipher.decrypt("ABC", 3), "XYZ")

    def test_non_alphabetic_characters(self):
        # Numbers and special characters should be preserved by default
        self.assertEqual(CaesarCipher.encrypt("Hello, World! 123", 3), "Khoor, Zruog! 123")
        self.assertEqual(CaesarCipher.decrypt("Khoor, Zruog! 123", 3), "Hello, World! 123")

    def test_large_and_negative_shifts(self):
        # Shift 29 is equivalent to shift 3 (29 % 26 = 3)
        self.assertEqual(CaesarCipher.encrypt("abc", 29), "def")
        self.assertEqual(CaesarCipher.encrypt("abc", -3), "xyz")
        self.assertEqual(CaesarCipher.decrypt("def", 29), "abc")
        self.assertEqual(CaesarCipher.decrypt("xyz", -3), "abc")

    def test_shift_numbers_setting(self):
        # When shift_numbers is True, 0-9 digits should be shifted modulo 10
        self.assertEqual(CaesarCipher.encrypt("abc129", 3, shift_numbers=True), "def452")
        self.assertEqual(CaesarCipher.decrypt("def452", 3, shift_numbers=True), "abc129")

    def test_brute_force(self):
        ciphertext = "Khoor, Zruog!"
        results = CaesarCipher.brute_force(ciphertext)
        self.assertEqual(len(results), 25)
        # Shift 3 decryption should match
        self.assertEqual(results[3], "Hello, World!")

if __name__ == "__main__":
    unittest.main()
