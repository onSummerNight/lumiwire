# Brief: Step 7d — validate checks edition before fields

**Goal:** `validate()` reads the MTI version digit before decoding any field; if it doesn't match the spec's edition, that is the single error returned.

**Why now:** 7c review: a 2003 message (2100) validated against the 1987 spec reports "field 52: no entry in spec", which hides the real cause (wrong edition). User chose this before the v2 wrap-up.

## Steps
1. `validate.py`: before calling `decode()`, read the MTI from the start of the hex per the spec's `mti_encoding` (ascii: 8 hex chars; bcd: 4). If it can't be read or isn't 4 digits, keep the existing MTI error. If the version digit doesn't match the edition, return only that error (it already names the edition); don't decode further.
2. Otherwise continue exactly as now (decode, then content checks).
3. Tests in `tests/test_2003.py`: MSG_2100 against the 1987 spec → exactly one error, the version-digit one; MSG_2800 likewise; a 1987 message against the 2003 spec → the version-digit error. Existing validate tests unchanged.
4. Small commit: `fix: validate reports wrong edition before field errors`.

## Acceptance check
`.venv/bin/pytest -q`: all pass (62 existing + new edition-mismatch tests).

## Constraints
- Don't change `decode()`, `encode()`, `mask()` or the CLI. Reuse existing MTI-reading code if `decode.py` has a helper; don't duplicate parsing logic beyond the MTI.
- Synthetic data only.

## Out of scope
Same check inside `decode` / CLI `decode`, choosing the spec automatically from the MTI, v2.0 wrap-up (next brief).

## Result
Done. `validate()` peeks the MTI (reusing `_Reader`/`_read_digits` from decode) and returns only the version-digit error on mismatch.
`.venv/bin/pytest -q` → `64 passed in 0.03s` (62 + 2 net new: 2100 and 2800 vs 1987 spec, 1987 msg vs 2003 spec; the old 2100 test was tightened to exactly one error).
Decision for manager: `test_collects_all_errors` relied on version-digit + content error together, which the brief's rule makes impossible. I changed its base to `bad_mti_nondigit` (still 2 errors). Brief said existing validate tests unchanged.
