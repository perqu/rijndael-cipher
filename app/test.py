import unittest
import cipher

class TestCipher(unittest.TestCase):

    def test_one_word(self):
        text = 'python'

        key = '0123456789abcdef'

        cipher.add_key(key)
        encoded_message = cipher.encode_message(text)

        cipher.add_key(key)
        decoded_message = cipher.decode_message(encoded_message)
        self.assertEqual(decoded_message, text)

    def test_two_word(self):
        text = 'python language'

        key = '0123456789abcdef'

        cipher.add_key(key)
        encoded_message = cipher.encode_message(text)

        cipher.add_key(key)
        decoded_message = cipher.decode_message(encoded_message)
        self.assertEqual(decoded_message, text)

    def test_digits_word(self):
        text = '1234567890'

        key = '0123456789abcdef'

        cipher.add_key(key)
        encoded_message = cipher.encode_message(text)

        cipher.add_key(key)
        decoded_message = cipher.decode_message(encoded_message)
        self.assertEqual(decoded_message, text)

    def test_all_ascii(self):
        text = ''
        for i in range(0,255):
            if i != 3:
                text += chr(i)

        key = '0123456789abcdef'

        cipher.add_key(key)
        encoded_message = cipher.encode_message(text)

        cipher.add_key(key)
        decoded_message = cipher.decode_message(encoded_message)
        self.assertEqual(decoded_message, text)

if __name__ == '__main__':
    unittest.main()