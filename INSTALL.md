# How to install

<details>
<summary><strong>Claude Code</strong></summary>

### Install

```bash
claude plugin marketplace add happycapybara1/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Type `/i-have-adhd`.

While the rules are on, a hook adds a one-line reminder of the response shape to each message you send, so the rules do not fade in long sessions. It turns off with "stop adhd mode". Hooks need `node` on your `PATH`.

### Verify

```bash
claude plugin list
```

### Update

```bash
claude plugin marketplace update i-have-adhd
claude plugin update i-have-adhd@i-have-adhd
```

The first command refreshes the marketplace listing. The second updates the installed plugin. Restart Claude Code to load it.

`claude plugin update` skips a plugin whose `version` has not changed. If you maintain a fork, bump `version` in `.claude-plugin/plugin.json` after you edit the rules.

### Uninstall

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
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
codex plugin marketplace add happycapybara1/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

Invoke the skill explicitly by typing `$i-have-adhd`. Codex will not activate
it automatically.

### Verify

```bash
codex plugin list
```

### Update

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### Uninstall

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### Always-on (optional)

Add to `~/.codex/AGENTS.md`:

```markdown
## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. First line: the result if you did the work, or the next action (command, path, or snippet) if the reader must act. If anything is left open, end with one next action doable in under two minutes.
2. Number multi-step work; one bounded action per step.
3. Finish the current issue before raising a new one.
4. Restate progress each turn ("step 3 of 5 done").
5. Give time estimates only for steps the reader does, in concrete units.
6. After a change, show what now works.
7. Errors: location, cause, fix. If the evidence does not show the cause, say "cause unknown" and give the next diagnostic step.
8. Show at most 5 items per list, then "N more: ... Want them?"
9. No preamble, no recaps, no closers.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.
```

</details>


<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI has no plugin marketplace, so there are two native routes: a **custom command** (opt-in, off until you invoke it) or an **extension** (always-on once installed). The command route matches this skill's default posture; pick it unless you want the rules on every session.

### Install (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/happycapybara1/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

Start a new session, type `/i-have-adhd`. It stays on for that session.

### Install (extension, always-on)

```bash
gemini extensions install https://github.com/happycapybara1/i-have-adhd
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
gemini extensions update i-have-adhd    # extension route
# command route: re-run the curl above
```

### Uninstall

```bash
gemini extensions uninstall i-have-adhd    # extension route
rm ~/.gemini/commands/i-have-adhd.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

Copilot reads Agent Skills natively: the same `SKILL.md`, no conversion. It scans `.github/skills/`, `.claude/skills/`, and `.agents/skills/` in the project, and `~/.copilot/skills/`, `~/.claude/skills/`, and `~/.agents/skills/` globally.

### Install

```bash
npx skills add happycapybara1/i-have-adhd -a github-copilot        # this project
npx skills add happycapybara1/i-have-adhd -a github-copilot -g     # all projects
```

Without the CLI, copy the skill folder into any directory Copilot scans:

```bash
git clone https://github.com/happycapybara1/i-have-adhd
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

The reader has ADHD. Shape every response so it can be acted on:

1. First line: the result if you did the work, or the next action (command, path, or snippet) if the reader must act. If anything is left open, end with one next action doable in under two minutes.
2. Number multi-step work; one bounded action per step.
3. Finish the current issue before raising a new one.
4. Restate progress each turn ("step 3 of 5 done").
5. Give time estimates only for steps the reader does, in concrete units.
6. After a change, show what now works.
7. Errors: location, cause, fix. If the evidence does not show the cause, say "cause unknown" and give the next diagnostic step.
8. Show at most 5 items per list, then "N more: ... Want them?"
9. No preamble, no recaps, no closers.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.
```

</details>


<details>
<summary><strong>OpenCode</strong></summary>

The plugin supports OpenCode V1 **1.18.29+** and V2. It registers the skill and `/i-have-adhd` command, and adds optional always-on mode. Older V1 versions need an upgrade or the plugin from the previous skill release.

### Install

For use across projects:

```bash
git clone https://github.com/happycapybara1/i-have-adhd ~/.config/opencode/vendor/i-have-adhd
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
2. **You invoke it explicitly.** Type `/i-have-adhd` in Claude Code, Copilot, Gemini CLI, or OpenCode, or `$i-have-adhd` in Codex. Rules stay on for that session. In Claude Code, a hook repeats a one-line reminder of the response shape on every message. "stop adhd mode" or "normal mode" turns them off.
3. **You turn on always-on.** Claude Code: `touch ~/.claude/.i-have-adhd-always`. OpenCode: `touch ~/.config/opencode/.i-have-adhd-always`. Gemini CLI: install the extension route. Codex and Copilot: paste the always-on snippet from their section.

If you did not turn it on, it is off.

## Troubleshooting

**`/i-have-adhd` not in autocomplete.** Restart the agent. The plugin index is read at startup.

**Always-on flag has no effect.** Update the plugin (`claude plugin marketplace update i-have-adhd`, then `claude plugin update i-have-adhd@i-have-adhd`) and restart. Hooks are read at startup.

**`claude plugin marketplace add` fails.** Use the `owner/repo` form. A local path must point at the repo root, not `.claude-plugin/`.

**Installed but replies still preamble.** Open a new session. If it still drifts, tighten the wording in `skills/i-have-adhd/SKILL.md`.

**Switching from the upstream plugin to this fork.** Both share the same names, so remove the upstream copy first:

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
claude plugin marketplace add happycapybara1/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Restart, then re-invoke `/i-have-adhd`.

**Skill missing after `npx skills add`.** Start a new agent chat. Skills are indexed at session start. Confirm the folder landed where your agent scans and that the frontmatter `name` matches the folder name.
