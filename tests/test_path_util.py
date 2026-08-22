"""Tests for currency_converter.path_util."""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from currency_converter.path_util import (
    _normalize_path,
    add_to_posix_user_path,
    add_to_windows_user_path,
    ensure_path,
    get_scripts_dir,
    is_in_path,
)


class TestPathUtil(unittest.TestCase):
    def test_get_scripts_dir_returns_nonempty_string(self):
        scripts_dir = get_scripts_dir()
        self.assertIsInstance(scripts_dir, str)
        self.assertTrue(len(scripts_dir) > 0)

    def test_normalize_path(self):
        p = os.path.join("a", "b", "c")
        norm = _normalize_path(p)
        self.assertIsInstance(norm, str)

    def test_is_in_path(self):
        fake_path = os.path.abspath("test_fake_bin_dir")
        with patch.dict(os.environ, {"PATH": f"{fake_path}{os.pathsep}/usr/bin"}):
            self.assertTrue(is_in_path(fake_path))
            self.assertFalse(is_in_path("definitely_not_in_path_12345"))

    def test_add_to_windows_user_path_non_windows(self):
        if sys.platform != "win32":
            added, msg = add_to_windows_user_path("/fake/path")
            self.assertFalse(added)
            self.assertIn("Not a Windows system", msg)

    def test_add_to_posix_user_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            target_dir = str(tmp_path / "fake_scripts")
            fake_home = tmp_path / "home"
            fake_home.mkdir()
            fake_bashrc = fake_home / ".bashrc"
            fake_bashrc.write_text("")

            with patch("pathlib.Path.home", return_value=fake_home):
                added, msg = add_to_posix_user_path(target_dir)
                self.assertTrue(added)
                content = fake_bashrc.read_text()
                self.assertIn(target_dir, content)

                # Running a second time should detect it's already there
                added2, msg2 = add_to_posix_user_path(target_dir)
                self.assertFalse(added2)

    def test_ensure_path(self):
        added, msg = ensure_path(silent=True)
        self.assertIsInstance(added, bool)
        self.assertIsInstance(msg, str)


if __name__ == "__main__":
    unittest.main()
