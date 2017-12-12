# -*- coding: utf-8 -*-
from unittest import TestCase, skip

from url_shortener.hashing import Base62_Hasher


class TestHasher(TestCase):
    def setUp(self):
        self.hasher = Base62_Hasher()

    def test_invalid_inputs(self):
        id = 0

        try:
            encoded_string = self.hasher.encode(id)
        except Exception as e:
            self.assertTrue(isinstance(e, ValueError))

        id = -1

        try:
            encoded_string = self.hasher.encode(id)
        except Exception as e:
            self.assertTrue(isinstance(e, ValueError))

    def test_single_digit_input(self):
        id = 1

        expected_encoded_string = 'b'

        encoded_string = self.hasher.encode(id)
        self.assertEqual(expected_encoded_string, encoded_string)
        decoded_string = self.hasher.decode(encoded_string)
        self.assertEqual(id, decoded_string)

    def test_double_digit_input(self):
        id = 21

        expected_encoded_string = 'v'

        encoded_string = self.hasher.encode(id)
        self.assertEqual(expected_encoded_string, encoded_string)
        decoded_string = self.hasher.decode(encoded_string)
        self.assertEqual(id, decoded_string)

    def test_longer_input(self):
        id = 95769

        expected_encoded_string = 'P4y'

        encoded_string = self.hasher.encode(id)
        self.assertEqual(expected_encoded_string, encoded_string)
        decoded_string = self.hasher.decode(encoded_string)
        self.assertEqual(id, decoded_string)

    def test_id_with_repeated_digit_to_anticipate_obfuscation_breakage(self):
        id = 33333

        expected_encoded_string = 'NPi'

        encoded_string = self.hasher.encode(id)
        self.assertEqual(expected_encoded_string, encoded_string)
        decoded_string = self.hasher.decode(encoded_string)
        self.assertEqual(id, decoded_string)

    def test_long_number(self):
        id = 9223372036854775807

        expected_encoded_string = 'hWifIaXiv9k'

        encoded_string = self.hasher.encode(id)
        self.assertEqual(expected_encoded_string, encoded_string)
        decoded_string = self.hasher.decode(encoded_string)
        self.assertEqual(id, decoded_string)
