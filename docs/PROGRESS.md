# Progress

## Done
- Scaffold created
- Context agreed and LOCKED 2026-10-07
- Step 1: skeleton, Typer CLI stubs, JSON spec loader, demo 1987 spec (fields 2,3,4,11,35,39,41,70). 3 tests pass.
- Decided: JSON spec; masking moved into step 2
- Step 2a: `decode()` in `src/lumiwire/decode.py` (MTI, primary/secondary bitmap, ASCII/BCD, fixed/llvar/lllvar, `DecodeError`). 8 tests pass.

## Now
- Nothing in progress.

## Next
2b. Masking of PAN and track data (default on, explicit flag to unmask) and CLI `decode` wiring. Test: masked output never contains a full synthetic PAN.
3. Encode from JSON, with round-trip tests (decode then encode gives the same bytes)

## Later
- Validate command and broken-message tests (in v1 scope, after step 3)
- Diff two messages field by field
- Test-vector generation (valid and broken)
- Optional Claude explain mode
- ISO 8583:1993 and :2003

## Blockers
- None
