# Contributing

Keep API documentation grounded in source filenames and line numbers. Preserve exact spellings even when firmware contains a typo. Distinguish archived source, installed firmware, static checks, host mocks and actual hardware execution.

## Local checks

Use Python 3.11+ and Node.js 22+. Create a Python virtual environment and install requirements-dev.txt, then run:

```sh
npm ci
python -m unittest discover -s tests -p "test_*.py" -v
python test_swerve.py
npm test
npm run typecheck
python tools/check_repository.py
```

Use your virtual environment's Python for USB operations. CI never connects to a device. The negative type-check fixture intentionally contains errors; check_repository verifies that the expected diagnostics remain enabled.

## Refreshing source-derived hints

Never import the original hardware modules on desktop Python. Keep source-library unchanged and retain licence headers. Generate into a separate output directory:

```sh
python tools/generate_sdk.py --source source-library --output .cache/generated
```

Review generated changes and update evidence/SOURCE_MANIFEST.json only after comparing original byte hashes. The VGA workaround is indexing-only; it must never modify the archive. The generator's generated docs directory is temporary, not this repository's root guide layout.

## Releases

Update package.json, vscode-extension/package.json and CHANGELOG.md together. After all checks pass:

```sh
python tools/build_release.py
```

Outputs in dist include a VSIX, a portable project archive and SHA256SUMS.txt. Install the VSIX locally and run Kepoco: Check IntelliSense in a trusted test workspace before describing actual editor behavior as verified. Releases do not flash firmware or update the device's runtime.
