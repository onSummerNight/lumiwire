# Context: LumiWire

Status: LOCKED 2026-10-07

## Problem

ISO 8583 messages are dense binary or hex. Reading one or building a valid one takes a custom script every time.

## Users

Developers and testers who work on card payment systems: switches, acquirers, issuers, terminal software.

## Scope v1

- Decode a hex message into readable fields; encode from JSON back to hex
- Field definitions in a spec file, so dialects are configuration, not code
- Validate a message against the spec
- Mask card numbers and track data in all output by default
- CLI with `decode`, `encode`, `validate` commands

## Non-goals

- Diff, test-vector generation, Claude explain mode (all in Later)
- Network switch or host simulation
- Cryptography: PIN blocks, MAC, key management
- Any real card data or real network specifications
- ISO 8583:1993 and :2003, NDC and other ATM protocols

## Success check

- Round-trip tests: decode then encode gives the same bytes, on a set of synthetic messages
- Validate rejects a set of deliberately broken synthetic messages with a clear error
- Masked output never contains a full synthetic PAN (tested)

## Stack

Python 3.10+, standard library plus Typer, pytest. Same layout as LumiLog.

## Constraints

- Clean room: only the public ISO 8583 structure and synthetic data. No scheme or bank message specifications.
- ISO 8583:1987 only. Primary and secondary bitmap. Fields in ASCII-hex or BCD.
- Masking on by default; unmasking needs an explicit flag.

## Open questions

- Exact spec file format (JSON or TOML): decide at step 1
