"""Checks installation paths in INSTALL.md."""

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ClaudeCodeUpdateTest(unittest.TestCase):
    def test_marketplace_refresh_is_paired_with_plugin_update(self):
        # `claude plugin marketplace update` refreshes only the marketplace
        # listing; the installed copy stays at its old version until
        # `claude plugin update` runs, so the docs must never offer the first alone.
        refresh = "claude plugin marketplace update i-have-adhd"
        update = "claude plugin update i-have-adhd@i-have-adhd"
        for path in [ROOT / "INSTALL.md"]:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf8")
                self.assertIn(update, text)
                for block in re.split(r"\n[^\S\n]*\n", text):
                    if refresh in block:
                        self.assertIn(update, block)


if __name__ == "__main__":
    unittest.main()
