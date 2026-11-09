// Shared by the i-have-adhd hooks: where a session's on/off state lives, and the
// skill text to inject when something other than the slash command turns the
// mode on (the "adhd mode" phrase, or ticking "ADHD mode" in a question).

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const claudeDir = () => process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");

export const alwaysOn = () => fs.existsSync(path.join(claudeDir(), ".i-have-adhd-always"));

// null for a missing or unsafe session id (it becomes a file name).
export function sessionState(sessionId) {
  if (typeof sessionId !== "string" || !/^[A-Za-z0-9_-]{1,128}$/.test(sessionId)) return null;
  const stateDir = process.env.CLAUDE_PLUGIN_DATA
    ? path.join(process.env.CLAUDE_PLUGIN_DATA, "sessions")
    : path.join(claudeDir(), ".i-have-adhd-sessions");
  const statePath = path.join(stateDir, sessionId);
  return {
    get: () => (fs.existsSync(statePath) ? fs.readFileSync(statePath, "utf8").trim() : ""),
    set: (value) => {
      fs.mkdirSync(stateDir, { recursive: true });
      fs.writeFileSync(statePath, value);
    },
  };
}

export const TURNED_ON =
  'i-have-adhd mode is now on for this session ("stop adhd mode" turns it off). ' +
  "Say so in one short line at the top of this reply. The ruleset below applies to every response.";

// The skill text without its frontmatter.
export function skillBody() {
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const skillPath = path.join(scriptDir, "..", "skills", "i-have-adhd", "SKILL.md");
  return fs
    .readFileSync(skillPath, "utf8")
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, "")
    .replace(/(?:\r?\n)+$/, "");
}
