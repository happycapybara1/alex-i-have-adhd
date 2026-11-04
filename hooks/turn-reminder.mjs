// UserPromptSubmit hook: adds a one-line reminder of the response shape to
// every prompt while i-have-adhd is on, so the rules stay in view after the
// full skill text has scrolled far back or been compacted away.
//
// On when: the reader invoked the skill this session (/i-have-adhd,
// /alex-i-have-adhd:i-have-adhd, or Codex's $i-have-adhd), or the always-on flag
// $CLAUDE_CONFIG_DIR/.i-have-adhd-always exists. Off after "stop adhd mode"
// or "normal mode" until the skill is invoked again.
// Never blocks the prompt: any failure exits 0 with no output.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const REMINDER =
  "i-have-adhd mode is on for this session; the reader has ADHD. " +
  "Response shape: the first line is the result (when you did the work) or the next action (when the reader must act). " +
  "Multi-step work is a numbered list. Lists show at most 5 items. " +
  "When a multi-step task is in progress, the reply states which step is done and which is next. " +
  "If anything is left open, the last line names one next step. " +
  "No preamble, recap, or closing pleasantries.";

const INVOKE = /^\s*[/$](?:(?:alex-)?i-have-adhd:)?i-have-adhd(?=\s|$)/i;
const STOP = /\b(?:stop adhd mode|normal mode)\b/i;
const PASTED = /<pasted_content id="[^"]*">[\s\S]*?<\/pasted_content id="[^"]*">/g;

function readStdin() {
  try {
    return fs.readFileSync(0, "utf8");
  } catch {
    return "";
  }
}

try {
  const input = JSON.parse(readStdin());
  const sessionId = input.session_id;
  const prompt = typeof input.prompt === "string" ? input.prompt : "";
  if (typeof sessionId !== "string" || !/^[A-Za-z0-9_-]{1,128}$/.test(sessionId)) process.exit(0);

  const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");
  const stateDir = process.env.CLAUDE_PLUGIN_DATA
    ? path.join(process.env.CLAUDE_PLUGIN_DATA, "sessions")
    : path.join(claudeDir, ".i-have-adhd-sessions");
  const statePath = path.join(stateDir, sessionId);
  const setState = (value) => {
    fs.mkdirSync(stateDir, { recursive: true });
    fs.writeFileSync(statePath, value);
  };

  if (INVOKE.test(prompt)) {
    // This turn already carries the full skill text.
    setState("on");
    process.exit(0);
  }
  if (STOP.test(prompt.replace(PASTED, ""))) {
    setState("off");
    process.exit(0);
  }

  const state = fs.existsSync(statePath) ? fs.readFileSync(statePath, "utf8").trim() : "";
  const alwaysOn = fs.existsSync(path.join(claudeDir, ".i-have-adhd-always"));
  if (state === "on" || (alwaysOn && state !== "off")) {
    process.stdout.write(REMINDER + "\n");
  }
} catch {
  // Never block the prompt.
}
process.exit(0);
