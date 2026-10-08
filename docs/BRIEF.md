# Brief: Step 9 — license, README footer, brief command

**Goal:** repo has an MIT `LICENSE`, the README ends with a "LumiDev project" footer linking to https://lumidev.online, and the pending `.claude/commands/brief.md` change is committed.

**Why now:** User instruction. `pyproject.toml` already declares `license = { text = "MIT" }` but no LICENSE file exists.

## Steps
1. `LICENSE`: standard MIT text, `Copyright (c) 2026 LumiDev` (matches `authors` in pyproject). No other wording changes.
2. README: append a footer after the last section, e.g. a `---` rule then `A [LumiDev project](https://lumidev.online) · MIT License`. Nothing else in the README changes.
3. Commit 1: `chore: add MIT license and LumiDev footer` (LICENSE, README.md).
4. Commit 2: `chore: update brief command to review-and-pick flow` (`.claude/commands/brief.md` only, as it is on disk; don't edit it).
5. Check: `git status --short` clean apart from docs; `.venv/bin/pytest -q` still 64 passed.

## Acceptance check
`head -3 LICENSE` shows "MIT License" and the 2026 LumiDev copyright; `tail -3 README.md` shows the footer link; `git status --short` shows no `.claude/` change; pytest 64 passed.

## Constraints
- No code, version or tag changes. Two separate commits as above.
- Do NOT push; report so the user can approve.

## Out of scope
License headers in source files, badges, a new release/tag, any other README edits.

## Result
Done. Two commits made, not pushed.
- `head -3 LICENSE`: "MIT License" / "Copyright (c) 2026 LumiDev"; README ends with the footer link.
- `git status --short`: no `.claude/` change; pytest: 64 passed.
- Note: commit `55c93d1 ci: run tests on push` (adds `.github/workflows`) landed between my commits; not from this task. Push needs your approval.
