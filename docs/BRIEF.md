# Brief: Step 8 — v2.0 wrap-up

**Goal:** README covers both editions and the new field features, verified in a fresh venv; version 2.0.0; tag `v2.0` locally.

**Why now:** v2 success check met (7c) and the wrong-edition error fixed (7d). Remaining gaps (tertiary bitmap, subfields, renumbering) need sources we don't have; they go to Later.

## Steps
1. README: "Editions" section (1987 default, 2003 via `--spec`, demo-not-normative warning), spec-format table includes `edition`, `b`, `llllvar`; one validate example of the wrong-edition error. Add `examples/2100.json` (synthetic, test PAN) and an encode/decode example with it.
2. Fresh venv in the scratchpad: `pip install -e .`, run every README command verbatim; outputs must match. Fix the README, not the code, unless a command is broken (then smallest fix plus a test, and report it).
3. `pyproject.toml` version `2.0.0`; `.venv/bin/pytest -q` green.
4. Move tertiary bitmap, subfields and field renumbering from Next to Later in PROGRESS, pointing at `docs/ISO2003-GAPS.md`.
5. Commit `docs: README and example for v2`, then `git tag v2.0` locally. Do NOT push; report so the user can approve.

## Acceptance check
Every README command in a fresh venv gives the output shown; `.venv/bin/pytest -q` → 64 passed; `git tag` lists `v2.0`.

## Constraints
- Synthetic data only; no real card numbers or hostnames. Keep `.claude/commands/brief.md` out of commits.
- Ask before pushing the commit or tag.

## Out of scope
Tertiary bitmap, subfields, renumbering, auto spec selection from MTI, PyPI, CI, GitHub release.

## Result
Done. All 8 README commands run verbatim in a fresh venv match the shown output; `.venv/bin/pytest -q` → 64 passed.
Added `examples/2100.json`, README Editions section and `edition` row in the spec table; version 2.0.0; tertiary bitmap/subfields/renumbering moved to Later.
No code changes. Commit `docs: README and example for v2` and local tag `v2.0` made, not pushed.
Decide: push `main` and tag `v2.0` to origin?
