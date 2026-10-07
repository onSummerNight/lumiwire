# Brief: Step 2b — masking + CLI `decode`

**Goal:** `lumiwire decode HEX` prints decoded fields with PAN and track data masked by default; `--unmask` shows them in full.

**Why now:** Top of Next. Completes step 2 and the success check "masked output never contains a full synthetic PAN".

## Steps
1. `src/lumiwire/mask.py`: `mask(result, spec) -> dict` returns a copy; fields with `sensitive == "pan"` keep first 6 and last 4 digits, the middle becomes `*`; `"track"` keeps first 6 and last 4 digits of the PAN part only, everything else becomes `*`. Values too short to mask safely are fully starred.
2. CLI `decode`: `--spec` defaults to the bundled `specs/iso8583_1987.json`; decode, mask unless `--unmask`, print one line per field (`MTI 0200`, then `002 Primary account number: 411111******1111`). `DecodeError`/`SpecError` → message on stderr, exit 1.
3. `tests/test_mask.py`: masked output for both synthetic messages contains no full PAN anywhere (check the digits run, not just the field); track data likewise; `--unmask` shows them in full.
4. CLI test with Typer's `CliRunner`: default output masked, exit 0; truncated message → exit 1 with an error.

## Acceptance check
`.venv/bin/pytest -q` — all pass (8 existing + new mask/CLI tests); `lumiwire decode <0200 hex>` shows `411111******1111`.

## Constraints
- Don't change `decode()` or its bitmap handling (see DECISIONS 2026-10-07).
- Masking happens before any output; no code path prints unmasked unless `--unmask`.
- Synthetic data only. Small commit: `feat: mask sensitive fields and wire decode CLI`.

## Out of scope
Encode, validate, JSON output format, `bitmap_encoding` handling.

## Result
Done. `.venv/bin/pytest -q` → `13 passed in 0.02s` (8 existing + 5 new).
`lumiwire decode <0200 hex>` prints `002 Primary account number: 411111******1111`; track 2 prints `411111******1111************`.
For manager: (1) track masking stars the separator and everything after the PAN. (2) Existing `test_cli_stub_runs` used `decode` as the not-implemented stub; it now uses `encode`. (3) PANs under 13 digits are fully starred.
