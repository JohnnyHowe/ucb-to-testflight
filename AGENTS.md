# Repository Guidelines

## Project Structure & Module Organization
This package is a Unity Editor-side tool for uploading iOS `.ipa` builds to TestFlight.

- `Editor/UploadToTestFlight/`: main upload flow (`upload_to_testflight.py`), env loading, and uploader logic.
- `Editor/UploadToTestFlight/testflight_uploader/`: configuration, key-file creation, build file discovery, and fastlane upload orchestration.
- `Editor/command_utility/`: command construction/execution helpers.
- `Editor/pretty_print.py`: shared colored logging utility.
- `upload_to_testflight.sh`: shell entrypoint used by local runs/CI.
- `example.env`: template for required environment variables.

Unity `.meta` files are part of package integrity; keep them in sync when adding or moving assets.

## Build, Test, and Development Commands
- `bash upload_to_testflight.sh`: standard entrypoint; runs the Python uploader.
- `python3 Editor/UploadToTestFlight/upload_to_testflight.py`: direct execution for debugging.
- `python3 -m py_compile Editor/**/*.py`: quick syntax validation pass before opening a PR.

Prerequisites: `fastlane` (`pilot upload`), Python 3, and optional `python-dotenv` when using a local `.env`.

## Coding Style & Naming Conventions
- Python style in this repo uses 4-space indentation and type hints where practical.
- Files/modules: `snake_case.py`; classes: `PascalCase`; functions/variables: `snake_case`.
- Keep logging readable and prefixed (existing pattern: component tag like `[TestFlightUploader]`).
- Prefer small, focused modules under `Editor/` rather than large multi-purpose scripts.

## Testing Guidelines
There is currently no dedicated automated test suite in this package. For contributions:

- Run `python3 -m py_compile Editor/**/*.py` to catch syntax/import issues.
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