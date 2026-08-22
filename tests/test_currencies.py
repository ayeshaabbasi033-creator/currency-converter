"""Tests for currency_converter.currencies."""

import unittest

from currency_converter.currencies import is_valid, suggest


class TestCurrencies(unittest.TestCase):
    def test_valid_code_uppercase(self):
        self.assertTrue(is_valid("USD"))

    def test_valid_code_lowercase(self):
        self.assertTrue(is_valid("pkr"))

    def test_invalid_code(self):
        self.assertFalse(is_valid("USF"))

    def test_suggest_single_char_typo(self):
        self.assertEqual(suggest("USF"), "USD")

    def test_suggest_transposition(self):
        self.assertEqual(suggest("UDS"), "USD")

    def test_suggest_no_close_match(self):
        self.assertIsNone(suggest("12345"))


if __name__ == "__main__":
    unittest.main()
