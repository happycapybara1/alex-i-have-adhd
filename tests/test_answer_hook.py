"""Ticking "ADHD mode" in a question (alex-ring asks one) turns the mode on."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTION = "Which plugins should I load for this session?"


@unittest.skipUnless(shutil.which("node"), "node is required for the hook")
class AnswerHookTest(unittest.TestCase):
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

    def run_hook(self, script, payload):
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        env["CLAUDE_PLUGIN_DATA"] = str(self.data_dir)
        result = subprocess.run(
            [shutil.which("node"), str(self.plugin_root / "hooks" / script)],
            input=payload if isinstance(payload, str) else json.dumps(payload),
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout

    def answer(self, picked, session_id="s1", options=("Superpowers", "Ponytail", "ADHD mode")):
        return self.run_hook("answer-on.mjs", {
            "session_id": session_id,
            "hook_event_name": "PostToolUse",
            "tool_name": "AskUserQuestion",
            "tool_input": {
                "questions": [{
                    "question": QUESTION,
                    "multiSelect": True,
                    "options": [{"label": label, "description": ""} for label in options],
                }],
                "answers": {QUESTION: picked},
            },
        })

    def test_ticking_adhd_mode_turns_it_on_with_the_rules(self):
        output = json.loads(self.answer("Superpowers, ADHD mode"))
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertEqual("PostToolUse", output["hookSpecificOutput"]["hookEventName"])
        self.assertIn("i-have-adhd mode is now on", context)
        self.assertIn("## Response shape", context)
        self.assertNotIn("disable-model-invocation", context)
        # Later turns get the per-turn reminder, as after /i-have-adhd.
        reminder = self.run_hook("turn-reminder.mjs", {"session_id": "s1", "prompt": "next question"})
        self.assertIn("first line", reminder.lower())

    def test_other_answers_change_nothing_even_though_the_option_was_offered(self):
        for picked in ("Superpowers, Ponytail", "Ponytail", ""):
            with self.subTest(picked=picked):
                self.assertEqual("", self.answer(picked, session_id="none"))
        self.assertEqual("", self.run_hook("turn-reminder.mjs", {"session_id": "none", "prompt": "next"}))

    def test_answer_in_the_tool_result_text_counts_too(self):
        output = self.run_hook("answer-on.mjs", {
            "session_id": "s2",
            "tool_name": "AskUserQuestion",
            "tool_input": {"questions": [{"question": QUESTION, "options": [{"label": "ADHD mode"}]}]},
            "tool_response": f'User has answered your questions: "{QUESTION}"="ADHD mode". You can now continue.',
        })
        self.assertIn("i-have-adhd mode is now on", output)

    def test_already_on_adds_nothing(self):
        self.run_hook("turn-reminder.mjs", {"session_id": "s3", "prompt": "/i-have-adhd"})
        self.assertEqual("", self.answer("ADHD mode", session_id="s3"))
        (self.config_dir / ".i-have-adhd-always").touch()
        self.assertEqual("", self.answer("ADHD mode", session_id="s4"))

    def test_ticking_turns_it_back_on_after_stop(self):
        self.run_hook("turn-reminder.mjs", {"session_id": "s5", "prompt": "stop adhd mode"})
        self.assertIn("i-have-adhd mode is now on", self.answer("ADHD mode", session_id="s5"))

    def test_bad_input_never_blocks(self):
        self.assertEqual("", self.run_hook("answer-on.mjs", "not json"))
        self.assertEqual("", self.answer("ADHD mode", session_id="../../etc"))

    def test_hooks_json_runs_it_after_questions(self):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        entries = config["hooks"]["PostToolUse"]
        self.assertEqual(["AskUserQuestion"], [entry["matcher"] for entry in entries])
        self.assertIn("answer-on.mjs", entries[0]["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main()
