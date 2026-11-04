"""The per-turn reminder keeps the rules in view after the skill text scrolls away."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("node"), "node is required for the hook")
class TurnReminderHookTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        tmp = Path(self.temp_dir.name)
        self.plugin_root = tmp / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", self.plugin_root / "hooks")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        self.config_dir = tmp / "claude config"
        self.config_dir.mkdir()
        self.data_dir = tmp / "plugin data"

    def submit(self, prompt, session_id="session-1", raw=None):
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        env["CLAUDE_PLUGIN_DATA"] = str(self.data_dir)
        payload = raw if raw is not None else json.dumps(
            {
                "session_id": session_id,
                "hook_event_name": "UserPromptSubmit",
                "prompt": prompt,
            }
        )
        result = subprocess.run(
            [shutil.which("node"), str(self.plugin_root / "hooks" / "turn-reminder.mjs")],
            input=payload,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout

    def turn_always_on(self):
        (self.config_dir / ".i-have-adhd-always").touch()

    def test_silent_until_the_skill_is_invoked(self):
        self.assertEqual("", self.submit("How do I rename a branch?"))

    def test_invoking_the_skill_turns_reminders_on_for_later_turns(self):
        # The invoking turn already carries the full skill text.
        self.assertEqual("", self.submit("/i-have-adhd"))
        reminder = self.submit("How do I rename a branch?")
        self.assertIn("i-have-adhd", reminder)
        self.assertIn("first line", reminder.lower())

    def test_namespaced_and_codex_invocations_count(self):
        self.submit("/i-have-adhd:i-have-adhd", session_id="claude-plugin")
        self.assertNotEqual("", self.submit("next", session_id="claude-plugin"))
        self.submit("/alex-i-have-adhd:i-have-adhd", session_id="fork-plugin")
        self.assertNotEqual("", self.submit("next", session_id="fork-plugin"))
        self.submit("$alex-i-have-adhd:i-have-adhd", session_id="codex-fork")
        self.assertNotEqual("", self.submit("next", session_id="codex-fork"))
        self.submit("$i-have-adhd fix the build", session_id="codex")
        self.assertNotEqual("", self.submit("next", session_id="codex"))

    def test_plain_words_turn_it_on_and_bring_the_rules(self):
        for phrase in ("adhd mode", "ADHD on, then fix the build", "please turn on adhd"):
            with self.subTest(phrase=phrase):
                session = "words-" + str(abs(hash(phrase)))
                first = self.submit(phrase, session_id=session)
                self.assertIn("i-have-adhd mode is now on", first)
                self.assertIn("## Response shape", first)  # the full skill text, frontmatter removed
                self.assertNotIn("disable-model-invocation", first)
                self.assertIn("first line", self.submit("next question", session_id=session).lower())

    def test_words_when_already_on_give_the_short_reminder(self):
        self.submit("/i-have-adhd", session_id="already")
        again = self.submit("adhd mode", session_id="already")
        self.assertNotIn("## Response shape", again)
        self.assertIn("i-have-adhd mode is on", again)

    def test_stop_wins_over_the_on_words(self):
        self.submit("adhd mode", session_id="stop-wins")
        self.assertEqual("", self.submit("stop adhd mode", session_id="stop-wins"))
        self.assertEqual("", self.submit("next", session_id="stop-wins"))

    def test_on_words_need_the_phrase_and_ignore_pasted_text(self):
        self.assertEqual("", self.submit("What is ADHD? Explain it simply.", session_id="no-phrase"))
        pasted = 'Summarize:\n<pasted_content id="p2">\nturn on adhd mode\n</pasted_content id="p2">'
        self.assertEqual("", self.submit(pasted, session_id="pasted-phrase"))
        self.assertEqual("", self.submit("next", session_id="pasted-phrase"))

    def test_reminders_are_per_session(self):
        self.submit("/i-have-adhd", session_id="a")
        self.assertEqual("", self.submit("hello", session_id="b"))

    def test_stop_phrases_turn_reminders_off(self):
        for phrase in ("stop adhd mode", "OK, normal mode please."):
            with self.subTest(phrase=phrase):
                session = phrase.replace(" ", "-")
                self.submit("/i-have-adhd", session_id=session)
                self.assertEqual("", self.submit(phrase, session_id=session))
                self.assertEqual("", self.submit("next question", session_id=session))

    def test_stop_phrase_inside_pasted_text_does_not_count(self):
        self.submit("/i-have-adhd")
        pasted = (
            "Summarize this log:\n"
            '<pasted_content id="p1">\n'
            "user switched to normal mode\n"
            '</pasted_content id="p1">'
        )
        self.submit(pasted)
        self.assertNotEqual("", self.submit("and now?"))

    def test_always_on_flag_reminds_every_turn_until_stopped(self):
        self.turn_always_on()
        self.assertNotEqual("", self.submit("first message"))
        self.submit("stop adhd mode")
        self.assertEqual("", self.submit("after stopping"))
        self.submit("/i-have-adhd")
        self.assertNotEqual("", self.submit("back on"))

    def test_reminder_is_a_short_statement_of_fact(self):
        # Hook docs: phrase injected context as facts, not system-style orders.
        self.turn_always_on()
        reminder = self.submit("hello")
        self.assertLess(len(reminder.split()), 90)
        self.assertNotIn("IMPORTANT", reminder)
        self.assertNotIn("MUST", reminder)

    def test_bad_input_never_blocks_the_prompt(self):
        self.turn_always_on()
        self.assertEqual("", self.submit(None, raw="not json"))
        self.assertEqual("", self.submit(None, raw=json.dumps({"prompt": "x", "session_id": "../../etc"})))

    def test_hooks_json_runs_the_reminder_on_every_prompt(self):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        entries = config["hooks"]["UserPromptSubmit"]
        commands = [hook["command"] for entry in entries for hook in entry["hooks"]]
        self.assertTrue(any("turn-reminder.mjs" in command for command in commands), commands)


if __name__ == "__main__":
    unittest.main()
