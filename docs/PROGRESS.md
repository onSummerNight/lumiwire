# Progress

Updated 2026-10-08 08:11

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
- Step 7b: spec type `b` (raw bytes, hex in JSON) and length `llllvar` in decode/encode/validate; README spec table updated. 54 tests pass.
- Step 7c: bundled `iso8583_2003.json` demo spec (not normative), two synthetic 2003 messages, tests/test_2003.py, README Editions section. 62 tests pass.
- Step 7d: `validate()` checks the MTI edition before decoding; a wrong edition is the single error. 64 tests pass.
- Step 8: README Editions + spec table, `examples/2100.json`, all 8 README commands verified in a fresh venv; version 2.0.0; tag `v2.0`, both pushed to origin. 64 tests pass.
- Step 9: MIT `LICENSE`, README LumiDev footer, `brief.md` change committed; CI workflow (pytest on 3.10/3.12) added, first run green. All on origin. 64 tests pass.

## Now
- Nothing in progress. v2.0 + step 9 on origin.

## Next
- Nothing planned; see Later

## Later
- Diff two messages field by field
- Test-vector generation (valid and broken)
- Optional Claude explain mode
- ISO 8583:1993
- Tertiary bitmap, subfields, field renumbering for 2003 (need sources; see docs/ISO2003-GAPS.md)

## Blockers
- None. Note: `55c93d1` (CI workflow) was committed by another session during step 9; not reviewed here.
