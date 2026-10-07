# Brief: Step 5 — v1 wrap-up

**Goal:** a stranger can install LumiWire from a clean checkout and run `decode`, `encode` and `validate` by following `README.md`; v1.0 tagged locally.

**Why now:** All v1 scope is built and every success check passes (43 tests); the repo has no README. User chose wrap-up.

## Steps
1. `README.md` (short): what it is (from CONTEXT Problem), install (`pip install -e .`), one example each for decode (masked output), `--unmask`, encode from a JSON file, validate (OK and one error), spec file format (keys and allowed values from `spec.py`), clean-room note and "synthetic data only".
2. Add `examples/0200.json` (synthetic, test PAN) used by the README encode example.
3. Fresh venv in the scratchpad: `pip install -e .`, then run every README command verbatim; outputs must match what the README shows. Fix the README, not the code, unless a command is broken.
4. Check `pyproject.toml` has version `1.0.0` and the `lumiwire` entry point; `.venv/bin/pytest -q` still green.
5. Commit `docs: README and example for v1`, then `git tag v1.0` locally. Do NOT push; report so the user can approve.

## Acceptance check
Every README command run in a fresh venv gives the output shown; `.venv/bin/pytest -q` → 43 passed; `git tag` lists `v1.0`.

## Constraints
- No code changes unless a README command fails (then the smallest fix, with a test). Synthetic data only; no real card numbers or hostnames.
- Ask before pushing the commit or tag.

## Out of scope
Later items (diff, test vectors, explain mode, 1993/2003), PyPI publishing, CI setup.

## Result
Done. Fresh venv `pip install -e .`; all 5 README commands (encode, decode, decode --unmask, validate OK, validate error) output matched the README exactly.
`.venv/bin/pytest -q` -> `43 passed in 0.03s`. `git tag` lists `v1.0`.
- pyproject version was `0.1.0`; bumped to `1.0.0` (brief step 4). No code changes.
- Not pushed. Manager/user must approve pushing the commit and tag.
