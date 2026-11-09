# How to install

<details>
<summary><strong>Claude Code</strong></summary>

### Install

```bash
claude plugin marketplace add happycapybara1/alex-i-have-adhd
claude plugin install alex-i-have-adhd@alex-i-have-adhd
```

Type `/i-have-adhd`, or in Claude Code just say "adhd mode" (also "adhd on" or "turn on adhd"): the hook then loads the rules itself, and Claude confirms in one line.

While the rules are on, a hook adds a one-line reminder of the response shape to each message you send, so the rules do not fade in long sessions. It turns off with "stop adhd mode". Hooks need `node` on your `PATH`.

### Verify

```bash
claude plugin list
```

### Update

```bash
claude plugin marketplace update alex-i-have-adhd
claude plugin update alex-i-have-adhd@alex-i-have-adhd
```

The first command refreshes the marketplace listing. The second updates the installed plugin. Restart Claude Code to load it.

`claude plugin update` skips a plugin whose `version` has not changed. If you maintain a fork, bump `version` in `.claude-plugin/plugin.json` after you edit the rules.

### Uninstall

```bash
claude plugin uninstall alex-i-have-adhd@alex-i-have-adhd
claude plugin marketplace remove alex-i-have-adhd
```

Or keep it installed and turn it off: `claude plugin disable i-have-adhd`.

### Always-on (optional)

A `SessionStart` hook loads the full ruleset at the start of every session, no `/i-have-adhd` needed:

```bash
touch ~/.claude/.i-have-adhd-always
```

If you use a custom Claude configuration directory, create the flag there instead:

```bash
touch "$CLAUDE_CONFIG_DIR/.i-have-adhd-always"
```

Back to on-demand:

```bash
rm ~/.claude/.i-have-adhd-always
```

The hook only fires when the flag file exists, so installing the plugin changes nothing by itself. "stop adhd mode" still turns it off for the current session.

</details>


<details>
<summary><strong>Codex</strong></summary>

### Install

```bash
codex plugin marketplace add happycapybara1/alex-i-have-adhd --ref main
codex plugin add alex-i-have-adhd@alex-i-have-adhd
```

Invoke the skill explicitly by typing `$i-have-adhd`. Codex will not activate
it automatically.

### Verify

```bash
codex plugin list
```

### Update

```bash
codex plugin marketplace upgrade alex-i-have-adhd
codex plugin remove alex-i-have-adhd
codex plugin add alex-i-have-adhd@alex-i-have-adhd
```

### Uninstall

```bash
codex plugin remove alex-i-have-adhd
codex plugin marketplace remove alex-i-have-adhd
```

### Always-on (optional)

Add to `~/.codex/AGENTS.md`:

```markdown
## Output style

The reader has ADHD. Every response has this shape, leaving out empty parts:

1. First line: the result if you did the work, the action if the reader must act, the answer to a question, or a one-line summary when the reader asked for content (a plan, code, an explanation).
2. While a multi-step task is in progress: "Step 3 of 5 done: <what>. Next: <what>."
3. When the reader has more than one thing to do: a numbered list, one action per step, and a time estimate in concrete units for steps the reader does.
4. Only the detail the first line needs; when the reader asked for content, that content in full. Lists show at most 5 items, then "N more: <what they are>. Want them?"
5. If something is left open, the last line is one next step doable in under two minutes, or one question about a second issue.

Errors: what failed, the cause, the fix. If the evidence does not show the cause, say "cause unknown" and give the next diagnostic step. Start with part 1 and end after the last part that has content.

Exceptions: explain fully when asked to explain. Before a destructive action, ask for confirmation and name exactly what would be lost. After three failed fixes, name the doubtful assumption. If the request is ambiguous, ask one short question.
```

</details>


<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI has no plugin marketplace, so there are two native routes: a **custom command** (opt-in, off until you invoke it) or an **extension** (always-on once installed). The command route matches this skill's default posture; pick it unless you want the rules on every session.

### Install (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/happycapybara1/alex-i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

Start a new session, type `/i-have-adhd`. It stays on for that session.

### Install (extension, always-on)

```bash
gemini extensions install https://github.com/happycapybara1/alex-i-have-adhd
```

The extension loads `GEMINI.md`, which imports the full skill, so the rules apply from message one. `git` must be installed.

### Verify

```bash
gemini extensions list          # extension route
ls ~/.gemini/commands           # command route: i-have-adhd.toml present
```

Or type `/` in a session and confirm `i-have-adhd` is listed.

### Update

```bash
gemini extensions update alex-i-have-adhd    # extension route
# command route: re-run the curl above
```

### Uninstall

```bash
gemini extensions uninstall alex-i-have-adhd    # extension route
rm ~/.gemini/commands/i-have-adhd.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

Copilot reads Agent Skills natively: the same `SKILL.md`, no conversion. It scans `.github/skills/`, `.claude/skills/`, and `.agents/skills/` in the project, and `~/.copilot/skills/`, `~/.claude/skills/`, and `~/.agents/skills/` globally.

### Install

```bash
npx skills add happycapybara1/alex-i-have-adhd -a github-copilot        # this project
npx skills add happycapybara1/alex-i-have-adhd -a github-copilot -g     # all projects
```

Without the CLI, copy the skill folder into any directory Copilot scans:

```bash
git clone https://github.com/happycapybara1/alex-i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### Verify

Type `/` in the chat input and confirm `i-have-adhd` appears. Or:

```bash
npx skills list
npx skills ls -g    # if installed globally
```

### Update

```bash
npx skills update i-have-adhd
```

Or re-copy the folder after `git pull`.

### Uninstall

```bash
npx skills remove i-have-adhd
```

Or delete the `i-have-adhd` folder from the skills directory it landed in.

### Activation note

Copilot respects `disable-model-invocation`: nothing applies until you invoke the skill, same as Claude Code (tested in [#60](https://github.com/ayghri/i-have-adhd/pull/60)).

### Always-on (optional)

Add the block below to `.github/copilot-instructions.md` in the project (Copilot reads it into every chat):

```markdown
## Output style

The reader has ADHD. Every response has this shape, leaving out empty parts:

1. First line: the result if you did the work, the action if the reader must act, the answer to a question, or a one-line summary when the reader asked for content (a plan, code, an explanation).
2. While a multi-step task is in progress: "Step 3 of 5 done: <what>. Next: <what>."
3. When the reader has more than one thing to do: a numbered list, one action per step, and a time estimate in concrete units for steps the reader does.
4. Only the detail the first line needs; when the reader asked for content, that content in full. Lists show at most 5 items, then "N more: <what they are>. Want them?"
5. If something is left open, the last line is one next step doable in under two minutes, or one question about a second issue.

Errors: what failed, the cause, the fix. If the evidence does not show the cause, say "cause unknown" and give the next diagnostic step. Start with part 1 and end after the last part that has content.

Exceptions: explain fully when asked to explain. Before a destructive action, ask for confirmation and name exactly what would be lost. After three failed fixes, name the doubtful assumption. If the request is ambiguous, ask one short question.
```

</details>


<details>
<summary><strong>OpenCode</strong></summary>

The plugin supports OpenCode V1 **1.18.29+** and V2. It registers the skill and `/i-have-adhd` command, and adds optional always-on mode. Older V1 versions need an upgrade or the plugin from the previous skill release.

### Install

For use across projects:

```bash
git clone https://github.com/happycapybara1/alex-i-have-adhd ~/.config/opencode/vendor/i-have-adhd
mkdir -p ~/.config/opencode/plugins
cat > ~/.config/opencode/plugins/i-have-adhd.js <<'EOF'
export { default } from '../vendor/i-have-adhd/.opencode/plugins/i-have-adhd.mjs';
EOF
```

For an existing V1 installation, keep the `plugin` entry in `opencode.json`. If switching to the loader above, remove that entry.

Start a new session and type `/i-have-adhd`. The rules apply until you say `stop adhd mode` or `normal mode`.

#### Skill and command only (without always-on)

Alternatively, from a checkout, copy the skill and command into OpenCode's global directories:

```bash
mkdir -p ~/.config/opencode/skills/i-have-adhd ~/.config/opencode/commands
cp skills/i-have-adhd/SKILL.md ~/.config/opencode/skills/i-have-adhd/SKILL.md
cp .opencode/command/i-have-adhd.md ~/.config/opencode/commands/i-have-adhd.md
```

### Verify

Start OpenCode, type `/`, and confirm `i-have-adhd` appears in the command list.

### Update

```bash
git -C ~/.config/opencode/vendor/i-have-adhd pull
```

For the copy-based install, pull your checkout and re-copy the two files.

### Uninstall

Remove `~/.config/opencode/plugins/i-have-adhd.js`. For the copy-based install, remove `~/.config/opencode/skills/i-have-adhd/` and `~/.config/opencode/commands/i-have-adhd.md`. For an existing V1 config-based install, remove its `plugin` entry.

### Always-on (optional)

Requires the plugin. The flag adds the complete ruleset to the system prompt on every turn:

```bash
touch ~/.config/opencode/.i-have-adhd-always
```

`stop adhd mode` or `normal mode` asks the agent to return to its normal style for the current session. Delete the flag to stop automatic injection:

```bash
rm ~/.config/opencode/.i-have-adhd-always
```

If `XDG_CONFIG_HOME` is set, replace `~/.config` in these paths with that directory.

</details>

## How activation works

1. **Installed, not invoked.** Nothing happens until you invoke the skill. Claude Code and Copilot honor `disable-model-invocation: true` in `SKILL.md`; Codex honors `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
2. **You invoke it explicitly.** Type `/i-have-adhd` in Claude Code, Copilot, Gemini CLI, or OpenCode, or `$i-have-adhd` in Codex. In Claude Code, saying "adhd mode" works too, and so does ticking "ADHD mode" when [alex-ring](https://github.com/happycapybara1/alex-plugins) asks which plugins to load. Rules stay on for that session. In Claude Code, a hook repeats a one-line reminder of the response shape on every message. "stop adhd mode" or "normal mode" turns them off.
3. **You turn on always-on.** Claude Code: `touch ~/.claude/.i-have-adhd-always`. OpenCode: `touch ~/.config/opencode/.i-have-adhd-always`. Gemini CLI: install the extension route. Codex and Copilot: paste the always-on snippet from their section.

If you did not turn it on, it is off.

## Troubleshooting

**`/i-have-adhd` not in autocomplete.** Restart the agent. The plugin index is read at startup.

**Always-on flag has no effect.** Update the plugin (`claude plugin marketplace update alex-i-have-adhd`, then `claude plugin update alex-i-have-adhd@alex-i-have-adhd`) and restart. Hooks are read at startup.

**`claude plugin marketplace add` fails.** Use the `owner/repo` form. A local path must point at the repo root, not `.claude-plugin/`.

**Installed but replies still preamble.** Open a new session. If it still drifts, tighten the wording in `skills/i-have-adhd/SKILL.md`.

**Switching from the upstream plugin to this fork.** Remove the upstream copy (named `i-have-adhd`) first, so the rules don't load twice:

```bash
claude plugin uninstall i-have-adhd@i-have-adhd
claude plugin marketplace remove i-have-adhd
claude plugin marketplace add happycapybara1/alex-i-have-adhd
claude plugin install alex-i-have-adhd@alex-i-have-adhd
```

Restart, then re-invoke `/i-have-adhd`.

**Skill missing after `npx skills add`.** Start a new agent chat. Skills are indexed at session start. Confirm the folder landed where your agent scans and that the frontmatter `name` matches the folder name.
