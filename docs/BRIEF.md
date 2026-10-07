# Brief: Step 2a — decode core (library only)

**Goal:** `decode(hex_message, spec) -> dict` in `src/lumiwire/decode.py` that parses MTI, primary and secondary bitmap, and every field in the demo spec (ASCII and BCD, fixed/llvar/lllvar).

**Why now:** Top of Next. Step 2 is too large for one brief, so it is split: 2a decode core, 2b masking + CLI `decode` wiring.

## Steps
1. Bitmap: read primary (16 hex chars); if bit 1 set, read secondary. Return the sorted list of present field numbers. Error on a field with no spec entry.
2. Field parser: fixed/llvar/lllvar lengths; ASCII = 2 hex chars per char; BCD = 2 digits per byte, left-padded to even length (prefix in the same encoding as the field). Raise a clear `DecodeError` with field number and offset on short or trailing data.
3. Result shape: `{"mti": "0200", "fields": {2: "...", 3: "...", ...}}`. No masking yet.
4. Build synthetic test messages in `tests/messages.py` by hand (hex strings with a comment per part): one 0200 with fields 2,3,4,11,35,41; one 0800 with a secondary bitmap and field 70. Use test PANs only (e.g. 4111111111111111).
5. `tests/test_decode.py`: decode both messages to the expected dicts; truncated message and unknown field each raise `DecodeError`.

## Acceptance check
`pytest -q` — all tests pass (3 existing + new decode tests).

## Constraints
- Standard library only; reuse `Spec`/`Field` from `spec.py`, don't change its API.
- Synthetic data only. Clean room.
- Small commit: `feat: decode MTI, bitmaps and fields`.

## Out of scope
Masking, CLI wiring, encode, validate, type checking of field contents (n/an/ans) beyond what parsing needs.

## Result
Done. `.venv/bin/pytest -q` → `8 passed in 0.02s` (3 existing + 5 decode tests).
Decisions for manager: (1) bitmap is read as 8 raw bytes = 16 hex chars of input, per the brief, regardless of spec `bitmap_encoding` ("hex"/"binary" not distinguished yet). (2) llvar/lllvar length counts digits/chars, not bytes; BCD values are left-padded to a whole byte and the pad is stripped on decode (field 70 → "001").
