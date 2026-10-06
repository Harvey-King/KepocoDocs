# Third-party notices

KepocoDocs is an unofficial community reference and development kit. It is not endorsed by the University of Kent, TinyCircuits or Microsoft.

## Original Kepoco and Thumby source snapshot

`source-library/` retains the 17 user-supplied Python files without modification. SHA-256 provenance is recorded in `evidence/SOURCE_MANIFEST.json`; public paths are repository-relative. Sources are for reference and static analysis, not a verified replacement firmware bundle. Do not upload this directory to your device.

Several source headers identify TinyCircuits' Thumby API and credit Mason Watmough, Jason Marcum and Ben Rose under GNU GPL version 3 or later. The grayscale layer credits Keith Greenhow; SSD1306 refers to Timendus' grayscale implementation. Original notices and references remain in each file. Some supplied drivers have no explicit licence header; no new licence for those files is asserted here. Review their upstream/course permissions before further redistribution. Their inclusion preserves the existing source snapshot bundled with the original repository's VSIX.

Newly authored documentation, generator, hints, examples and extension code are provided under GPL-3.0-or-later, without warranty. This does not override third-party terms. Full GPL text is in LICENSE and licenses/GPL-3.0.txt.

## Supplemental MicroPython editor stubs

The vendored editor-only packages are micropython-rp2-rpi_pico-stubs 1.29.0.post1 and micropython-stdlib-stubs 1.29.0.post2. Package metadata, LICENSE.md files and typeshed licence/attributions remain under vendor/micropython. typings/time/__init__.pyi is copied from the vendored time.pyi to expose MicroPython ticks helpers rather than desktop time.

These are an RP2 editor baseline, not proof of a particular handheld's firmware or installed features.

Package origins:
- https://pypi.org/project/micropython-rp2-rpi_pico-stubs/
- https://pypi.org/project/micropython-stdlib-stubs/

## Separately installed tools

VS Code, Microsoft Python, Pylance and mpremote are separately installed dependencies, not firmware shipped by this project. Their own terms apply. The VSIX is distributed through this repository's releases, not the VS Code Marketplace.
