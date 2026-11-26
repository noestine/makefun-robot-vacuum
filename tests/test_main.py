"""Tests for the robot vacuum excuse entry (main.py).

The program must write exactly ONE line to /output/entry.txt:
1-120 characters, single line, UTF-8, not only whitespace.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PY = os.path.join(REPO_ROOT, "main.py")
OUTPUT_PATH = "/output/entry.txt"

EXPECTED_LINE = (
    "I skipped that spot because the dust bunny unionized, "
    "and I respect a picket line."
)


def run_program(cwd=REPO_ROOT):
    """Run main.py as a subprocess; return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, MAIN_PY],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestEntryOutput(unittest.TestCase):
    def test_program_exits_zero(self):
        result = run_program()
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_output_file_exists(self):
        run_program()
        self.assertTrue(os.path.isfile(OUTPUT_PATH))

    def test_exact_expected_line(self):
        """Deterministic: the program always writes the same excuse."""
        run_program()
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, EXPECTED_LINE)

    def test_single_line(self):
        run_program()
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn("\n", content)
        self.assertNotIn("\r", content)
        self.assertEqual(len(content.splitlines()), 1)

    def test_length_within_limits(self):
        run_program()
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertGreaterEqual(len(content), 1)
        self.assertLessEqual(len(content), 120)

    def test_not_only_whitespace(self):
        run_program()
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertTrue(content.strip(), "entry must not be only whitespace")

    def test_valid_utf8(self):
        run_program()
        with open(OUTPUT_PATH, "rb") as f:
            raw = f.read()
        raw.decode("utf-8")  # raises UnicodeDecodeError if invalid

    def test_deterministic_across_runs(self):
        run_program()
        with open(OUTPUT_PATH, "rb") as f:
            first = f.read()
        run_program()
        with open(OUTPUT_PATH, "rb") as f:
            second = f.read()
        self.assertEqual(first, second)

    def test_creates_output_dir_when_missing(self):
        """No crash if /output does not exist yet; the program creates it."""
        import shutil

        if os.path.isdir("/output"):
            shutil.rmtree("/output")
        result = run_program()
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(os.path.isfile(OUTPUT_PATH))


class TestValidateLine(unittest.TestCase):
    """Unit tests for the validation helper in main.py."""

    def setUp(self):
        sys.path.insert(0, REPO_ROOT)
        import main

        self.main = main

    def tearDown(self):
        sys.path.pop(0)
        sys.modules.pop("main", None)

    def test_valid_line_passes(self):
        self.assertTrue(self.main.validate_line(EXPECTED_LINE))

    def test_empty_line_rejected(self):
        with self.assertRaises(ValueError):
            self.main.validate_line("")

    def test_whitespace_only_rejected(self):
        with self.assertRaises(ValueError):
            self.main.validate_line("   \t  ")

    def test_over_limit_rejected(self):
        with self.assertRaises(ValueError):
            self.main.validate_line("x" * 121)

    def test_exactly_120_accepted(self):
        self.assertTrue(self.main.validate_line("x" * 120))

    def test_multiline_rejected(self):
        with self.assertRaises(ValueError):
            self.main.validate_line("first line\nsecond line")

    def test_write_entry_to_custom_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "entry.txt")
            self.main.write_entry(EXPECTED_LINE, path)
            with open(path, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), EXPECTED_LINE)

    def test_write_entry_rejects_bad_line_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "entry.txt")
            with self.assertRaises(ValueError):
                self.main.write_entry("", path)
            self.assertFalse(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
