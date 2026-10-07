# Progress

## Done
- Scaffold created
- Context agreed and LOCKED 2026-10-07
- Step 1: skeleton, Typer CLI stubs, JSON spec loader, demo 1987 spec (fields 2,3,4,11,35,39,41,70). 3 tests pass.
- Decided: JSON spec; masking moved into step 2
- Step 2a: `decode()` in `src/lumiwire/decode.py` (MTI, primary/secondary bitmap, ASCII/BCD, fixed/llvar/lllvar, `DecodeError`). 8 tests pass.
- Step 2b: `mask.py` (PAN/track masked by default) and CLI `decode` with `--unmask`. 13 tests pass.
- Step 3: `encode()` in `src/lumiwire/encode.py`, `EncodeError`, CLI `encode`, round-trip tests. 22 tests pass.
- Step 4a: `bitmap_encoding` honoured in decode/encode (binary, hex); demo spec set to binary. 24 tests pass.
- Step 4b: `validate()` in `src/lumiwire/validate.py`, CLI `validate`, 7 broken synthetic messages. 43 tests pass.
- Step 5: README.md, examples/0200.json, version 1.0.0; README commands verified in a fresh venv; tagged v1.0 locally (not pushed).

## Now
- Nothing in progress.

## Next
- User approval to push the v1.0 commit and tag

## Later
- Diff two messages field by field
- Test-vector generation (valid and broken)
- Optional Claude explain mode
- ISO 8583:1993 and :2003

## Blockers
- None
