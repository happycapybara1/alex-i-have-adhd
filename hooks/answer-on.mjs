// PostToolUse hook for AskUserQuestion: when the user ticks "ADHD mode" (alex-ring's
// question offers it), turn i-have-adhd on for this session and give Claude the
// rules, as saying "adhd mode" does. The skill is manual-only, so Claude can't
// load it itself. A multi-select answer is one string of comma-joined labels.
// Never blocks the tool call: any failure exits 0 with no output.

import fs from "node:fs";
import { TURNED_ON, alwaysOn, sessionState, skillBody } from "./session-state.mjs";

const TICKED = /(?:^|,)\s*adhd mode\s*(?:,|$)/i;

// Only the answers, never the question's option list.
function answers(data) {
  const out = [];
  const take = (map) => {
    if (map && typeof map === "object") {
      for (const value of Object.values(map)) if (typeof value === "string") out.push(value);
    }
  };
  take(data.tool_input && data.tool_input.answers);
  const response = data.tool_response;
  if (response && typeof response === "object") take(response.answers);
  if (typeof response === "string") {
    // 'User has answered your questions: "Which ...?"="Superpowers, ADHD mode". ...'
    for (const match of response.matchAll(/"="([^"]*)"/g)) out.push(match[1]);
  }
  return out;
}

try {
  const data = JSON.parse(fs.readFileSync(0, "utf8"));
  const state = sessionState(data.session_id);
  if (state && answers(data).some((answer) => TICKED.test(answer))) {
    const current = state.get();
    if (current !== "on" && !(alwaysOn() && current !== "off")) {
      state.set("on");
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "PostToolUse",
            additionalContext: TURNED_ON + "\n\n" + skillBody(),
          },
        }) + "\n",
      );
    }
  }
} catch {
  // Never block a tool call.
}
process.exit(0);
