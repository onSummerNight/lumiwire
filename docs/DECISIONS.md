# Decisions

Append-only. Date, decision, why, alternatives rejected.


2026-10-07 | Lock v1 scope: decode, encode, spec file, validate, default masking, CLI. ISO 8583:1987 only, Python 3.10+ with Typer. | A first version small enough to prove with round-trip tests. | Go (loses LumiLog layout); including diff, test vectors and Claude mode in v1 (too big); 1993/2003 editions (later).
2026-10-07 | Spec file format is JSON. Default masking of PAN and track data moves from Later into step 2 (still inside v1 scope; reorder only). | JSON needs no extra dependency on Python 3.10 and is easy to generate; masking from the first decode means no output path ever exists unmasked. | TOML (tomllib is 3.11+, writing needs a dependency); masking after step 3.
