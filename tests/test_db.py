"""Tests for currency_converter.db, run against an in-memory SQLite DB."""

import sqlite3
import unittest

from currency_converter.db import (
    SCHEMA,
    cache_rate,
    get_cached_rate,
    get_history,
    log_conversion,
)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.executescript(SCHEMA)

    def tearDown(self):
        self.conn.close()

    def test_cache_rate_roundtrip(self):
        cache_rate(self.conn, "usd", "pkr", 278.5)
        self.assertEqual(get_cached_rate(self.conn, "USD", "PKR"), 278.5)

    def test_get_cached_rate_missing_returns_none(self):
        self.assertIsNone(get_cached_rate(self.conn, "USD", "EUR"))

    def test_cache_rate_overwrites_existing_pair(self):
        cache_rate(self.conn, "usd", "pkr", 278.5)
        cache_rate(self.conn, "usd", "pkr", 280.0)
        self.assertEqual(get_cached_rate(self.conn, "usd", "pkr"), 280.0)

    def test_log_and_get_history(self):
        log_conversion(self.conn, 100, "usd", "pkr", 278.5, 27850.0)
        rows = get_history(self.conn, limit=5)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], 100)
        self.assertEqual(rows[0][5], 27850.0)

    def test_history_newest_first(self):
        log_conversion(self.conn, 10, "usd", "eur", 0.86, 8.6)
        log_conversion(self.conn, 20, "usd", "eur", 0.86, 17.2)
        rows = get_history(self.conn, limit=5)
        self.assertEqual(rows[0][1], 20)
        self.assertEqual(rows[1][1], 10)

    def test_history_respects_limit(self):
        for i in range(5):
            log_conversion(self.conn, i, "usd", "eur", 0.86, i * 0.86)
        rows = get_history(self.conn, limit=2)
        self.assertEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()
