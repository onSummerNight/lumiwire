# Progress

Updated 2026-10-07 21:38

## Done
- Context LOCKED 2026-10-07; JSON spec format
- Step 1: skeleton, Typer CLI, JSON spec loader, demo 1987 spec
- Step 2: `decode()` (MTI, primary/secondary bitmap, ASCII/BCD, fixed/llvar/lllvar) + masking of PAN/track by default (`--unmask`)
- Step 3: `encode()` from JSON, round-trip tests
- Step 4: `bitmap_encoding` honoured (binary/hex); `validate()` + broken-message tests
- Step 5: README + `examples/0200.json`, verified in a fresh venv; version 1.0.0
- Step 6: `main` and tag `v1.0` pushed to origin. 43 tests pass.
- All v1 success checks met.
- Step 7a: spec `edition` key (1987/2003), validate checks MTI version digit per edition, `docs/ISO2003-GAPS.md` written (field-level rows unverified). 46 tests pass.

## Now
- Nothing in progress. v1 complete.

## Next
- v2 (ISO 8583:2003 alongside 1987, decided 2026-10-07): 7a spec edition + MTI version check + 2003 gap list (briefed)

## Later
- Diff two messages field by field
- Test-vector generation (valid and broken)
- Optional Claude explain mode
- ISO 8583:1993

## Blockers
- None. Note: `.claude/commands/brief.md` has an uncommitted local edit (not ours; left untouched).
