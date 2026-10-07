# ISO 8583:2003 gaps vs current spec format

Public sources only, summarised (no standard text copied). Written 2026-10-07.
Sources: https://en.wikipedia.org/wiki/ISO_8583 (fetched); https://www.ir.com/guides/introduction-to-iso-8583 and
https://www.spark.money/glossary/iso-8583 (search snippets only, not fetched). Field-level detail is not in these
sources, so every row below about specific fields is **unverified**; confirm before sizing a 2003 spec brief.

Current spec supports: types n/an/ans/z; length fixed/llvar/lllvar; ascii/bcd; fields 2..128; one flat level.

| Gap | What | Fields | Size |
|---|---|---|---|
| Binary data type `b` | Raw-byte fields (e.g. MAC, keys); needs a type and hex in/out | 64, 128 in 1987; more in 2003 (unverified) | S |
| `llllvar` and longer prefixes | Wikipedia says later editions allow longer length indicators, esp. for binary | unverified which | S |
| Tertiary bitmap | Presence of fields 129..192; spec loader caps at 128 | 129..192 (rarely used per source) | M |
| Subfields / composite fields | 2003 introduces sub-elements inside data elements; spec is flat | unverified (amounts known: currency becomes a sub-element) | L |
| Field renumbering | Field placement differs between editions; currency elements of 1987/1993 unused in 2003 | currency fields (e.g. 49/50/51 in 1987, unverified) | M |
| Other type letters `a`, `s`, `x+n` | Standard lists a (alpha) and s (special); only an/ans exist here | unverified | S |
| Per-edition field tables | Fields differ per edition, so a 2003 spec file is a separate field list, not a delta | all | M |
| MTI version digit | Handled in step 7a (edition key: 1987 -> 0, 2003 -> 2) | MTI | done |

## Notes
- 1993 stays out of scope (DECISIONS 2026-10-07).
- Next brief should first obtain a field list from a public source (not a scheme spec) before building `iso8583_2003.json`.
