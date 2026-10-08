# Brief: Step 7c — 2003 demo spec

**Goal:** bundled `src/lumiwire/specs/iso8583_2003.json` (edition 2003) works end to end: synthetic 2003 messages round-trip, validate and mask.

**Why now:** User chose this after 7b. It meets the v2 success check in CONTEXT; field tables stay unverified (DECISIONS 2026-10-07).

## Steps
1. Spec: `"name": "iso8583-2003-demo"`, `"edition": "2003"`, `"description"` or top note saying "demo, not normative; field formats unverified". About 8 fields: 2 (PAN, llvar, sensitive pan), 3, 4, 11, 35 (track, sensitive), 41, one `b` fixed field, one `llllvar` field, plus one field > 64 so the secondary bitmap is used. If the loader rejects an unknown note key, put the note in `name` or README instead; don't change the loader for it.
2. `tests/messages.py`: two synthetic 2003 messages (MTI `2100` and `2800`, the second with a secondary bitmap), hex commented per part, test PAN only.
3. `tests/test_2003.py`: round-trip both ways; validate → `[]`; masked decode contains no full PAN or track; the 2003 message validated against the 1987 spec gives the version-digit error.
4. README: a short "Editions" line showing `--spec` with the 2003 file and the not-normative warning.
5. Small commit: `feat: ISO 8583:2003 demo spec`.

## Acceptance check
`.venv/bin/pytest -q`: all pass (54 existing + new 2003 tests).

## Constraints
- No code changes expected; if one is truly needed, smallest fix plus a test, and report it.
- Clean room: no field formats copied from the standard or a scheme spec. Synthetic data only.

## Out of scope
Choosing the spec automatically from the MTI version digit, tertiary bitmap, subfields, a full 2003 field table.

## Result
Done. `.venv/bin/pytest -q` → 62 passed (54 existing + 8 new in tests/test_2003.py). No code changes needed; loader ignores the `description` key.
Manager: MSG_2100 against the 1987 spec gives "field 52: no entry in spec" (decode fails before the version check), so the version-digit test uses MSG_2800 only; 2100 is tested for rejection. Docs commit is local, not pushed.
