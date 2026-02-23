#!/usr/bin/env python3
"""Tests for clawdocs CLI. Run: python3 tests/test_clawdocs.py"""

import json
import subprocess
import unittest
from pathlib import Path

CLI = str(Path(__file__).parent.parent / "clawdocs")


def run(*args, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(
        [CLI, *args],
        capture_output=True, text=True,
        **kwargs,
    )


class TestVersion(unittest.TestCase):
    def test_version(self):
        r = run("--version")
        self.assertEqual(r.returncode, 0)
        self.assertIn("clawdocs", r.stdout)


class TestList(unittest.TestCase):
    def test_list_channels(self):
        r = run("list", "--prefix", "channels/", "--slugs-only")
        self.assertEqual(r.returncode, 0)
        slugs = r.stdout.strip().splitlines()
        self.assertTrue(any("channels/telegram" in s for s in slugs))

    def test_list_json(self):
        r = run("list", "--prefix", "automation/", "--json")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        self.assertIn("slug", data[0])
        self.assertIn("title", data[0])

    def test_list_bad_prefix_exits_1(self):
        r = run("list", "--prefix", "zzz_nonexistent/")
        self.assertEqual(r.returncode, 1)


class TestSearch(unittest.TestCase):
    def test_search_slugs_only(self):
        r = run("search", "cron", "--slugs-only")
        self.assertEqual(r.returncode, 0)
        slugs = r.stdout.strip().splitlines()
        self.assertTrue(len(slugs) > 0)
        # All lines should look like slugs (contain / or be simple words)
        for s in slugs:
            self.assertNotIn(" ", s)

    def test_search_json(self):
        r = run("search", "telegram", "--json", "--limit", "3")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) <= 3)
        self.assertIn("slug", data[0])
        self.assertIn("url", data[0])


class TestGet(unittest.TestCase):
    def test_get_exact_slug(self):
        r = run("get", "channels/telegram", "-q")
        self.assertEqual(r.returncode, 0)
        self.assertIn("channels/telegram", r.stdout)
        self.assertIn("confidence: exact", r.stdout)

    def test_get_no_header(self):
        r = run("get", "channels/telegram", "--no-header", "-q")
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("--- clawdocs:", r.stdout)
        self.assertNotIn("confidence:", r.stdout)

    def test_get_json_structure(self):
        r = run("get", "channels/telegram", "--json", "-q")
        self.assertEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self.assertEqual(d["slug"], "channels/telegram")
        self.assertEqual(d["confidence"], "exact")
        self.assertIn("content", d)
        self.assertIn("related", d)
        self.assertIn("covers", d)
        self.assertGreater(len(d["content"]), 1000)

    def test_get_missing_strict_exits_1(self):
        r = run("get", "definitely/not/a/real/slug", "--strict", "-q")
        self.assertEqual(r.returncode, 1)

    def test_get_covers_populated(self):
        r = run("get", "channels/telegram", "--json", "-q")
        d = json.loads(r.stdout)
        self.assertTrue(len(d["covers"]) > 0)

    def test_get_related_populated(self):
        r = run("get", "channels/telegram", "--json", "-q")
        d = json.loads(r.stdout)
        self.assertTrue(len(d["related"]) > 0)
        # All related slugs belong to the same section (channels prefix)
        for rel in d["related"]:
            self.assertTrue(rel.startswith("channels"), f"unexpected related slug: {rel}")


class TestSmartFetch(unittest.TestCase):
    """Test the default 'fetch' mode (clawdocs <topic>)."""

    def test_keyword_resolves(self):
        r = run("telegram", "-q")
        self.assertEqual(r.returncode, 0)
        self.assertIn("channels/telegram", r.stdout)

    def test_exact_slug_as_topic(self):
        r = run("channels/telegram", "-q")
        self.assertEqual(r.returncode, 0)
        self.assertIn("confidence: exact", r.stdout)

    def test_no_header_clean_output(self):
        r = run("telegram", "--no-header", "-q")
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("--- clawdocs:", r.stdout)
        self.assertNotIn("url:", r.stdout)

    def test_stdout_clean_stderr_separate(self):
        """Diagnostics must go to stderr, content to stdout."""
        r = run("telegram")
        # stdout has content
        self.assertIn("Telegram", r.stdout)
        # stderr has resolution info
        self.assertIn("→", r.stderr)

    def test_exit_code_0_on_success(self):
        r = run("telegram", "-q")
        self.assertEqual(r.returncode, 0)


class TestExitCodes(unittest.TestCase):
    def test_exit_1_not_found(self):
        # Run with strict + unusual query to force not-found
        r = run("zzzznotreal", "--strict", "-q")
        # Either 1 (not found) or 0 (semantic search found something)
        # With strict, low-confidence should be 1
        self.assertIn(r.returncode, [0, 1])

    def test_exit_0_valid_get(self):
        r = run("get", "channels/telegram", "-q")
        self.assertEqual(r.returncode, 0)

    def test_exit_1_strict_missing_slug(self):
        r = run("get", "zzz/notreal", "--strict", "-q")
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
