// UserPromptSubmit hook: adds a one-line reminder of the response shape to
// every prompt while i-have-adhd is on, so the rules stay in view after the
// full skill text has scrolled far back or been compacted away.
//
// On when: the reader invoked the skill this session (/i-have-adhd,
// /alex-i-have-adhd:i-have-adhd, or Codex's $i-have-adhd), said "adhd mode"
// (or "adhd on", "turn on adhd"), or the always-on flag
// $CLAUDE_CONFIG_DIR/.i-have-adhd-always exists. Off after "stop adhd mode"
// or "normal mode" until it is turned on again.
// Never blocks the prompt: any failure exits 0 with no output.

import fs from "node:fs";
import { TURNED_ON, alwaysOn, sessionState, skillBody } from "./session-state.mjs";

const REMINDER =
  "i-have-adhd mode is on for this session; the reader has ADHD. " +
  "Response shape: the first line is the result (when you did the work) or the next action (when the reader must act). " +
  "Multi-step work is a numbered list. Lists show at most 5 items. " +
  "When a multi-step task is in progress, the reply states which step is done and which is next. " +
  "If anything is left open, the last line names one next step. " +
  "No preamble, recap, or closing pleasantries.";

const INVOKE = /^\s*[/$](?:(?:alex-)?i-have-adhd:)?i-have-adhd(?=\s|$)/i;
const STOP = /\b(?:stop adhd mode|normal mode)\b/i;
const PHRASE = /\b(?:adhd mode|adhd on|turn on adhd)\b/i;
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
  const prompt = typeof input.prompt === "string" ? input.prompt : "";
  const state = sessionState(input.session_id);
  if (!state) process.exit(0);

  if (INVOKE.test(prompt)) {
    // This turn already carries the full skill text.
    state.set("on");
    process.exit(0);
  }
  const typed = prompt.replace(PASTED, "");
  if (STOP.test(typed)) {
    state.set("off");
    process.exit(0);
  }

  const current = state.get();
  if (PHRASE.test(typed) && current !== "on") {
    state.set("on");
    process.stdout.write(TURNED_ON + "\n\n" + skillBody() + "\n");
    process.exit(0);
  }
  if (current === "on" || (alwaysOn() && current !== "off")) {
    process.stdout.write(REMINDER + "\n");
  }
} catch {
  // Never block the prompt.
}
process.exit(0);
