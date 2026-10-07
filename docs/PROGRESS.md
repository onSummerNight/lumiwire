# Progress

## Done
- Scaffold created
- Context agreed and LOCKED 2026-10-07
- Step 1: skeleton, Typer CLI stubs, JSON spec loader, demo 1987 spec (fields 2,3,4,11,35,39,41,70). 3 tests pass.
- Decided: JSON spec; masking moved into step 2

## Now
- Nothing in progress. Next session: `/continue-progress`, then step 2.

## Next
2. Decode: primary and secondary bitmap, field parsing for ASCII-hex and BCD, default masking of PAN and track data (explicit flag to unmask), synthetic test messages. Test: masked output never contains a full synthetic PAN.
3. Encode from JSON, with round-trip tests (decode then encode gives the same bytes)

## Later
- Validate command and broken-message tests (in v1 scope, after step 3)
- Diff two messages field by field
- Test-vector generation (valid and broken)
- Optional Claude explain mode
- ISO 8583:1993 and :2003

## Blockers
- None
