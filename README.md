# LumiWire

ISO 8583 messages are dense binary or hex. Reading one, or building a valid one, usually takes a custom script. LumiWire decodes, encodes and validates ISO 8583:1987 and :2003 messages from the command line, with field definitions in a JSON spec so dialects are configuration, not code.

Card numbers and track data are masked in all output by default.

**Synthetic data only.** This is a clean-room project built on the public ISO 8583 structure. Every message and card number here is made up; the bundled spec is a demo, not any scheme's or bank's specification.

## Install

Python 3.10+.

```
pip install -e .
```

## Use

Encode a JSON file (`examples/0200.json`) into a hex message:

```
lumiwire encode examples/0200.json
```
```
3032303070200000208000003136343131313131313131313131313131313030303030303030303030303030313030300001233238343131313131313131313131313131313D32353132313031303030305445524D30303031
```

Decode it. PAN and track data are masked:

```
lumiwire decode 3032303070200000208000003136343131313131313131313131313131313030303030303030303030303030313030300001233238343131313131313131313131313131313D32353132313031303030305445524D30303031
```
```
MTI 0200
002 Primary account number: 411111******1111
003 Processing code: 000000
004 Amount, transaction: 000000001000
011 STAN: 000123
035 Track 2 data: 411111******1111************
041 Terminal ID: TERM0001
```

Show them in full with `--unmask`:

```
lumiwire decode --unmask 3032303070200000208000003136343131313131313131313131313131313030303030303030303030303030313030300001233238343131313131313131313131313131313D32353132313031303030305445524D30303031
```
```
MTI 0200
002 Primary account number: 4111111111111111
003 Processing code: 000000
004 Amount, transaction: 000000001000
011 STAN: 000123
035 Track 2 data: 4111111111111111=25121010000
041 Terminal ID: TERM0001
```

Validate. A good message prints `OK` and exits 0:

```
lumiwire validate 3032303070200000208000003136343131313131313131313131313131313030303030303030303030303030313030300001233238343131313131313131313131313131313D32353132313031303030305445524D30303031
```
```
OK
```

A broken one (field 3 with an `A` in it) prints one error per line on stderr and exits 1:

```
lumiwire validate 3032303070200000208000003136343131313131313131313131313131313041303030303030303030303030313030300001233238343131313131313131313131313131313D32353132313031303030305445524D30303031
```
```
field 3 (Processing code): non-digit character 'A' in n field
```

All three commands take `--spec FILE` to use your own spec instead of the bundled one (`src/lumiwire/specs/iso8583_1987.json`). Validate quotes no value from PAN or track fields.

## Editions

Two editions are bundled. ISO 8583:1987 is the default. ISO 8583:2003 (MTI version digit 2) is selected with `--spec`:

```
lumiwire encode examples/2100.json --spec src/lumiwire/specs/iso8583_2003.json
```
```
3231303070200000208012003136343131313131313131313131313131313030303030303030303030303030313030300001233238343131313131313131313131313131313D32353132313031303030305445524D303030310123456789ABCDEF30303034DEADBEEF
```

```
lumiwire decode 3231303070200000208012003136343131313131313131313131313131313030303030303030303030303030313030300001233238343131313131313131313131313131313D32353132313031303030305445524D303030310123456789ABCDEF30303034DEADBEEF --spec src/lumiwire/specs/iso8583_2003.json
```
```
MTI 2100
002 Primary account number: 411111******1111
003 Processing code: 000000
004 Amount, transaction: 000000001000
011 STAN: 000123
035 Track 2 data: 411111******1111************
041 Terminal ID: TERM0001
052 Binary block: 0123456789ABCDEF
055 Binary variable data: DEADBEEF
```

The edition is not chosen from the MTI. Validating a 2003 message with the default 1987 spec reports the edition mismatch as the only error (exit 1):

```
lumiwire validate 3231303070200000208012003136343131313131313131313131313131313030303030303030303030303030313030300001233238343131313131313131313131313131313D32353132313031303030305445524D303030310123456789ABCDEF30303034DEADBEEF
```
```
MTI '2100': version digit must be 0 for ISO 8583:1987
```

**Warning:** the 2003 spec is a demo, not normative. Its field formats are unverified; known gaps are in `docs/ISO2003-GAPS.md`.

## Spec file

JSON, one file per dialect:

```json
{
  "name": "my-dialect",
  "mti_encoding": "ascii",
  "bitmap_encoding": "binary",
  "fields": {
    "2": {"name": "Primary account number", "type": "n", "length": "llvar", "max": 19, "encoding": "ascii", "sensitive": "pan"}
  }
}
```

| Key | Allowed values |
|---|---|
| `edition` | `1987`, `2003` (validate checks the MTI version digit against it) |
| `mti_encoding` | `ascii`, `bcd` |
| `bitmap_encoding` | `binary`, `hex` |
| field number (key) | 2 to 128 |
| `name` | any text |
| `type` | `n`, `an`, `ans`, `z`, `b` (raw bytes, hex in JSON and output; `max` counts bytes; `encoding` then applies to the length prefix only) |
| `length` | `fixed`, `llvar`, `lllvar`, `llllvar` (2, 3, 4-digit length prefix) |
| `max` | positive integer (the length for `fixed`) |
| `encoding` | `ascii`, `bcd` |
| `sensitive` (optional) | `pan`, `track` |

## Scope

ISO 8583:1987 and the :2003 demo spec, with primary and secondary bitmap. No cryptography (PIN blocks, MAC), no network simulation.

## Tests

```
pip install -e ".[dev]"
pytest -q
```
