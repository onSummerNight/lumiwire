# Log

Append-only. `YYYY-MM-DD HH:MM | who | what | result` (local time).

2026-10-07 19:00 | claude | Project scaffold created with a draft context | awaiting /kickoff
2026-10-07 21:10 | claude | /kickoff: CONTEXT.md rewritten and locked, PROGRESS.md and DECISIONS.md written | LOCKED
2026-10-07 22:00 | claude | Step 1: pyproject, Typer stub (decode/encode/validate), JSON spec loader + demo 1987 spec (8 fields), 3 pytest tests | 3 passed
2026-10-07 23:00 | claude | Step 2a: decode.py (MTI, bitmaps, ASCII/BCD, fixed/llvar/lllvar), tests/messages.py, tests/test_decode.py | 8 passed
2026-10-07 22:45 | manager | Review brief 2a (decode core: MTI, bitmaps, ASCII/BCD fields) | done, 8 passed (re-run); bitmap_encoding not honoured yet
2026-10-07 23:40 | claude | Step 2b: mask.py, CLI decode with --unmask, test_mask.py; test_spec stub test now uses encode | 13 passed
2026-10-07 23:20 | manager | Review brief 2b (masking + CLI decode) | done, 13 passed (re-run); track masks separator and discretionary data; step 2 complete
2026-10-07 23:59 | claude | Step 3: encode.py, CLI encode, test_encode.py; stub test now uses validate | 22 passed
2026-10-07 23:50 | manager | Review brief 3 (encode from JSON + round-trip) | done, 22 passed (re-run); step 3 complete
2026-10-07 | claude | Step 4a: honour bitmap_encoding (decode/encode), tests/spec_hex_bitmap.json, test_bitmap_encoding.py | 24 passed
2026-10-08 00:20 | manager | Review brief 4a (honour bitmap_encoding binary/hex) | done, 24 passed (re-run), existing tests unchanged
2026-10-07 | claude | Step 4b: validate.py, CLI validate, test_validate.py, BROKEN messages | 43 passed
2026-10-08 00:55 | manager | Review brief 4b (validate command + broken-message tests) | done, 43 passed (re-run); all v1 success checks covered
2026-10-07 | claude | Step 5: README, examples/0200.json, version 1.0.0, tag v1.0 (local) | 5 README commands match in fresh venv; 43 passed
2026-10-08 01:30 | manager | Review brief 5 (v1 wrap-up: README, example, tag) | done, README verified in fresh venv, 43 passed (re-run), v1.0 tagged locally, not pushed
2026-10-07 | claude | Step 6: clean-room grep, push main + v1.0 to origin | main d4ac320 and v1.0 b003cf1 match remote; no force
2026-10-07 21:37 | manager | Correction: manager review lines timed 22:45 to 01:30 (incl. "2026-10-08") had guessed timestamps; all happened on 2026-10-07 before 21:37. The push brief's "2026-10-08" approval date is the same error | dates fixed from here on
2026-10-07 21:37 | manager | Review brief 6 (push main + v1.0) | done, ls-remote matches (main d4ac320, v1.0 b003cf1); docs commit 0441c75 local only; v1 scope complete
2026-10-07 21:38 | manager | /save-progress: PROGRESS rewritten for v1 complete; docs committed and pushed | next session: /decide a Later item
2026-10-07 21:45 | user+manager | /decide: v2 adds ISO 8583:2003 alongside 1987; CONTEXT.md updated (scope, non-goals, constraints, success check) | approved
2026-10-07 21:46 | manager | Brief 7a written (spec edition + MTI version check + 2003 gap list) | handed to worker
2026-10-07 | claude | Step 7a: spec edition key, edition-aware MTI check, ISO2003-GAPS.md | 46 passed; gap list field details unverified
2026-10-07 21:53 | manager | Review brief 7a (spec edition + MTI version check + 2003 gap list) | done, 46 passed (re-run); gap list field rows unverified: no public 2003 field tables found
2026-10-07 21:55 | manager | Brief 7b written (binary type b + llllvar), user chose format features first | handed to worker
2026-10-08 | claude | Step 7b: type b + llllvar in spec/decode/encode/validate, tests, README | 54 passed
2026-10-08 07:59 | manager | Review brief 7b (binary type b + llllvar) | done, 54 passed (re-run); b encoding applies to length prefix only
2026-10-08 08:00 | manager | Brief 7c written (2003 demo spec, user choice) | handed to worker
2026-10-08 | claude | Step 7c: iso8583_2003.json demo spec, 2003 messages and tests, README Editions | 62 passed
2026-10-08 | claude | save-progress: 62 passed; commit v2 scope docs; push main | see git log
2026-10-08 08:01 | manager | Review brief 7c (2003 demo spec) | done, 62 passed (re-run), no code changes; wrong-edition message can fail on a field error before the version check; v2 success check met
2026-10-08 08:02 | manager | Brief 7d written (validate: edition check before field decode), user choice | handed to worker
2026-10-08 08:03 | claude | Step 7d: validate checks edition before decode; 3 new tests, 1 existing test re-based | 64 passed
2026-10-08 08:04 | manager | Review brief 7d (validate: edition check before fields) | done, 64 passed (re-run); test_collects_all_errors rebased on bad_mti_nondigit (accepted, still covers collect-all)
2026-10-08 08:05 | manager | Brief 8 written (v2.0 wrap-up: README, example, version, local tag) | handed to worker
2026-10-08 08:06 | claude | Step 8: README Editions/spec table, examples/2100.json, version 2.0.0, PROGRESS | 8 README commands match in fresh venv; 64 passed
2026-10-08 08:06 | claude | save-progress: pushed main and tag v2.0 to origin; PROGRESS updated | 64 passed
2026-10-08 08:06 | manager | Review brief 8 (v2.0 wrap-up) | done, 64 passed (re-run), README verified, main + v2.0 on origin match local; v2 scope complete, no new brief
2026-10-08 08:06 | manager | /save-progress: v2 complete, nothing in Next; next session starts with /decide on a Later item | committed
