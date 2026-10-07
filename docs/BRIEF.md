# Brief: Step 6 — publish v1.0

**Goal:** `main` (at or after b003cf1) and tag `v1.0` are on `origin` (github.com/onSummerNight/lumiwire).

**Why now:** v1 is complete and verified (43 tests, README checked in a fresh venv). User approved the push on 2026-10-08.

## Steps
1. `git status`: the only expected change is `.claude/commands/brief.md` plus docs. Commit docs if needed (`docs: v1 review and push brief`); leave `.claude/commands/brief.md` alone unless the user says otherwise.
2. Clean-room check before pushing: `git grep -nE '[0-9]{13,19}'` shows only hex runs and the test PAN 4111111111111111; no `.env`, keys or real hostnames tracked.
3. `git push origin main` then `git push origin v1.0`.
4. Verify: `git ls-remote --tags origin v1.0` and `git ls-remote origin main` match the local hashes.

## Acceptance check
`git ls-remote origin main refs/tags/v1.0` matches `git rev-parse main v1.0`.

## Constraints
- Push approval covers only `main` and `v1.0`. No force-push, no other branches or tags, no GitHub release or PyPI.
- If the push is rejected (remote ahead), stop and report; do not rebase or force.

## Out of scope
Later items (diff, test vectors, explain mode, 1993/2003): they need `/decide` first.

## Result
Done. `git ls-remote origin main refs/tags/v1.0` matches local:
d4ac3200… refs/heads/main = `git rev-parse main`
b003cf18… refs/tags/v1.0 = `git rev-parse v1.0` (lightweight tag; v1.0 was already on origin)
Clean-room grep: only hex runs and test PAN 4111111111111111; no .env/keys tracked.
Manager: brief's approval date (2026-10-08) was ahead of today (2026-10-07); user confirmed push. `.claude/commands/brief.md` left uncommitted. Result/progress commit is local, not pushed.
