# Repository Guidelines

## Project Structure & Module Organization
This package is a Unity Editor-side tool for uploading iOS `.ipa` builds to TestFlight.

- `src/ucb_to_testflight/`: main package (CLI entry, uploader flow, parameter loading, key-file lifecycle, build discovery, retry/error parsing).
- `tests/run_all.py`: lightweight smoke/syntax checks for package structure.
- `upload_to_testflight.sh`: shell entrypoint used by local runs/CI.
- `example.env`: template for required environment variables.

Unity `.meta` files are part of package integrity; keep them in sync when adding or moving assets.

## Build, Test, and Development Commands
- `bash upload_to_testflight.sh`: standard entrypoint; creates/uses `.venv`, installs deps, and runs the uploader.
- `.venv/bin/python3 -m ucb_to_testflight.upload_to_testflight_cmd_entry`: direct execution for debugging.
- `python3 -m py_compile src/ucb_to_testflight/*.py tests/run_all.py`: quick syntax validation pass before opening a PR.
- `python3 tests/run_all.py`: smoke check for package structure.

Prerequisites: `fastlane` (`pilot upload`), Python 3, and optional `python-dotenv` when using a local `.env`.

## Coding Style & Naming Conventions
- Python style in this repo uses 4-space indentation and type hints where practical.
- Files/modules: `snake_case.py`; classes: `PascalCase`; functions/variables: `snake_case`.
- Keep logging readable and prefixed (existing pattern: component tag like `[TestFlightUploader]`).
- Prefer small, focused modules under `src/ucb_to_testflight/` rather than large multi-purpose scripts.

## Testing Guidelines
There is currently a lightweight smoke check in this package. For contributions:

- Run `python3 -m py_compile src/ucb_to_testflight/*.py tests/run_all.py` to catch syntax/import issues.
- Run `python3 tests/run_all.py` from repo root.
- Perform a manual smoke test with a safe environment (`example.env` as baseline).
- Verify sensitive values (API key content) are never printed in logs.

## Commit & Pull Request Guidelines
Observed history uses short, single-line commit messages (for example, `Fixed typo`, `Removed printing api key content`).

- Use concise imperative commit messages (`Fix key parsing for multiline .p8`).
- Keep commits scoped to one logical change.
- PRs should include: purpose, changed paths, validation steps run, and any env var/secret handling impact.
- If uploader behavior changes, include a redacted sample command/log snippet in the PR description.

# Jons Notes
* make all planning docs in scratchpad folder
