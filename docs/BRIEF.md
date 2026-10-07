# Brief: Step 7a — 2003 gap list + edition-aware spec

**Goal:** the spec declares its edition, validate checks the MTI version digit against it, and `docs/ISO2003-GAPS.md` lists what 2003 needs beyond what the current spec format supports.

**Why now:** First v2 step (DECISIONS 2026-10-07). Find the real gaps before building a 2003 spec, so later briefs are sized on facts, not guesses.

## Steps
1. Spec loader: new required key `"edition"` in `{"1987", "2003"}`; MTI version digit is `"0"` for 1987, `"2"` for 2003. Add `"edition": "1987"` to the demo spec and both test spec files.
2. `validate.py`: replace the hard-coded `"0"` check with the spec's edition digit; error text names the edition.
3. Tests: spec without `edition` or with an unknown one → `SpecError`; a 1987-spec message with MTI `2100` → version-digit error; existing tests unchanged otherwise.
4. Write `docs/ISO2003-GAPS.md` (max 30 lines) from public sources only (cite URLs): for each 2003 feature the current spec can't express (e.g. other length-prefix sizes, binary fields, subfields/composite fields, field-number changes from 1987), one line with what it is, which fields use it, and a rough size (S/M/L). Mark anything uncertain as "unverified".
5. Small commit: `feat: spec edition and MTI version check`.

## Acceptance check
`.venv/bin/pytest -q`: all pass (43 existing + new edition tests), and `docs/ISO2003-GAPS.md` exists with sources.

## Constraints
- Clean room: public descriptions only. No copied text or tables from the ISO standard, no scheme specs. Synthetic data only.
- Don't change decode/encode/mask behaviour.

## Out of scope
The 2003 spec file itself and any gap implementation (later briefs, sized from the gap list).

## Result
Done. `.venv/bin/pytest -q` → 46 passed (43 + 3 new edition tests). Commit f28b41c; `docs/ISO2003-GAPS.md` written (23 lines, sources cited).
Manager: web sources gave no field-level 2003 detail, so field columns are marked unverified. Decide whether to find a public field list before the 2003 spec brief. Docs commit is local, not pushed.
