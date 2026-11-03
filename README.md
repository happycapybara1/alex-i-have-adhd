<p align="center">
  <img src="./logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHD-friendly outputs. No ADHD diagnosis needed!</strong>
</p>
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="License"></a>
</p>

> Fork of [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd), trimmed to 9 rules.

## Install

Copy/paste into your CLI prompt:

```text
Install the i-have-adhd skill/plugin from https://github.com/happycapybara1/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

Or 🔗 [check the installation instructions](INSTALL.md).

## What it does

A skill for your coding assistant that stops it from burying the answer. Action first. Steps numbered. No "Hope this helps!"

[Kacper Rutkiewicz | AI Made Simple](https://youtu.be/NEl8kPWZP_Y) has made a good breakdown of an earlier version of the skill.
## What changes


<table>
<tr>
<td width="50%">

## Before

> Great question! Let me think about this. Your auth flow has a few moving pieces: the middleware, the token verification, and the cookie handling. Looking at `src/auth.ts`, the `verifyToken` function (around lines 42-58) seems to be using an older `jsonwebtoken` API. One approach would be to update the package and rewrite that function. After making the change, you'd want to run the auth tests to confirm nothing breaks. By the way, you might also want to look at your dependency versions overall. Hope this helps! Let me know if you want to dig deeper.

</td>

<td width="50%">

## After

> Edit `src/auth.ts:42` to update the token validation.
>
> 1. Open `src/auth.ts`
> 2. Replace `verifyToken` (lines 42–58) with the snippet below
> 3. Run `npm test -- auth.spec.ts`
>
> Next: paste the first failing line if any test fails.

</td>
</tr>
</table>


## The rules

9 rules. Full text in [SKILL.md](./skills/i-have-adhd/SKILL.md).

1. First line: the result or the next action. Last line: one next step.
2. Number multi-step tasks.
3. Suppress tangents.
4. Restate state every turn.
5. Time estimates only for work you do yourself.
6. Make wins visible.
7. Errors: what failed, the cause (or "cause unknown"), the fix.
8. Show at most 5 items per list.
9. No preamble. No recap. No closers.

## Tune it

Fork, edit `skills/i-have-adhd/SKILL.md`, then swap your copy in:

```bash
claude plugin uninstall i-have-adhd            # drop the upstream copy first:
claude plugin marketplace remove i-have-adhd   # fork and upstream share both names
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Restart your coding assistant, then re-invoke `/i-have-adhd`.

## Credits

Loosely based on *The Adult ADHD Tool Kit* by J. Russell Ramsay and Anthony L. Rostain. Adapted for how an LLM should respond, not how a human should organize their day.

## License

[MIT](LICENSE).

Star ⭐ if it saved you one scroll past one "Great question!"
