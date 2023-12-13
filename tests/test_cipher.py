import unittest
import cipher  # Podmień to na właściwą nazwę modułu zawierającego implementację Cipher


class TestCipherFunctions(unittest.TestCase):
    def test_encode_with_valid_key(self):
        # Testuje, czy funkcja encode zwraca poprawną odpowiedź dla poprawnego klucza
        key = "0123456789abcdef"
        message = "Hello, World!"
        self.assertTrue(cipher.add_key(key))
        response = cipher.encode_message(message)
        self.assertIsNotNone(response)

    def test_encode_with_invalid_key(self):
        # Testuje, czy funkcja encode zwraca błąd dla niepoprawnego klucza
        key = "0123456789abcde"
        message = "Hello, World!"
        self.assertFalse(cipher.add_key(key))
        response = cipher.encode_message(message)
        self.assertEqual(response, None)

    def test_decode_with_valid_key(self):
        # Testuje, czy funkcja decode zwraca poprawną odpowiedź dla poprawnego klucza
        key = "0123456789abcdef"
        encoded_message = "207 97 215 47 91 50 229 127 35 142 125 151 113 253 245 178"
        self.assertTrue(cipher.add_key(key))
        response = cipher.decode_message(encoded_message)
        self.assertIsNotNone(response)

    def test_decode_with_invalid_key(self):
        # Testuje, czy funkcja decode zwraca błąd dla niepoprawnego klucza
        key = "0123456789abcde"
        encoded_message = "207 97 215 47 91 50 229 127 35 142 125 151 113 253 245 178"
        self.assertFalse(cipher.add_key(key))
        response = cipher.decode_message(encoded_message)
        self.assertEqual(response, None)

    def test_one_word(self):
        text = "python"
        key = "0123456789abcdef"

        cipher.add_key(key)
        encoded_message = cipher.encode_message(text)

        cipher.add_key(key)
        decoded_message = cipher.decode_message(encoded_message)
        self.assertEqual(decoded_message, text)

    def test_two_words(self):
        text = "python language"
        key = "0123456789abcdef"

        cipher.add_key(key)
        encoded_message = cipher.encode_message(text)

        cipher.add_key(key)
        decoded_message = cipher.decode_message(encoded_message)
        self.assertEqual(decoded_message, text)

    def test_all_ascii(self):
        text = ""
        for i in range(0, 255):
            if i != 3:
                text += chr(i)

        key = "0123456789abcdef"

        cipher.add_key(key)
        encoded_message = cipher.encode_message(text)

        cipher.add_key(key)
        decoded_message = cipher.decode_message(encoded_message)
        self.assertEqual(decoded_message, text)

    def test_different_key(self):
        text = "python"
        key = "0123456789abcdef"

        cipher.add_key(key)
        encoded_message = cipher.encode_message(text)

        key = "0123456789abcddd"

        cipher.add_key(key)
        decoded_message = cipher.decode_message(encoded_message)
        self.assertNotEqual(decoded_message, text)


if __name__ == "__main__":
    unittest.main()
