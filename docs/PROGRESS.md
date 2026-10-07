# Progress

## Done
- Scaffold created
- Context agreed and LOCKED 2026-10-07

## Now
- Nothing started. Next session: `/continue-progress`, then step 1.

## Next
1. Project skeleton (pyproject, Typer CLI stub, pytest) and spec file format decision (JSON vs TOML), with a 1987 spec covering a small field set
2. Decode: bitmap parsing (primary and secondary) and field parsing for ASCII-hex and BCD, with synthetic test messages
3. Encode from JSON, with round-trip tests (decode then encode gives the same bytes)

## Later
- Validate command and broken-message tests (in v1 scope, after step 3)
- Default masking of PAN and track data (in v1 scope, after step 3)
- Diff two messages field by field
- Test-vector generation (valid and broken)
- Optional Claude explain mode
- ISO 8583:1993 and :2003

## Blockers
- None
