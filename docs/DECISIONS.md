# Decisions

Append-only. Date, decision, why, alternatives rejected.


2026-10-07 | Lock v1 scope: decode, encode, spec file, validate, default masking, CLI. ISO 8583:1987 only, Python 3.10+ with Typer. | A first version small enough to prove with round-trip tests. | Go (loses LumiLog layout); including diff, test vectors and Claude mode in v1 (too big); 1993/2003 editions (later).
2026-10-07 | Spec file format is JSON. Default masking of PAN and track data moves from Later into step 2 (still inside v1 scope; reorder only). | JSON needs no extra dependency on Python 3.10 and is easy to generate; masking from the first decode means no output path ever exists unmasked. | TOML (tomllib is 3.11+, writing needs a dependency); masking after step 3.
2026-10-07 | Decode reads bitmaps as raw bytes (8 per bitmap) and ignores spec `bitmap_encoding` for now; variable lengths count digits/chars, BCD values left-padded to a whole byte with the pad stripped on decode. | Matches brief 2a and keeps decode simple; encode (step 3) must mirror exactly for round-trip. | Honouring `bitmap_encoding` now (deferred: demo spec says "hex" yet decode treats it as binary; resolve before validate).
2026-10-07 | Honour spec `bitmap_encoding`: "binary" = 8 raw bytes per bitmap, "hex" = 16 ASCII hex chars per bitmap. Demo spec set to "binary" (matches current behaviour). BCD fields reject non-digits whatever their type; empty `n` values rejected. | Dialects stay configuration as CONTEXT promises; resolves the 2a deferral before validate. | Binary only and drop the key (ASCII-bitmap dialects unrepresentable); reject "hex" and move on.
