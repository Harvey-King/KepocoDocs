# Kepoco Dev Kit

Unofficial source-derived VS Code support for the Kepoco library supplied by the user.

Features: Pylance completion and signatures, hover documentation with source locations, firmware caveats, eight Python snippets, API-reference commands, project setup and a real language-provider verification command. This is not an emulator, uploader, or desktop runtime implementation.

Open your game folder, then run **Kepoco: Set Up Current Project** from the command palette. This copies editor-only stubs and supplemental MicroPython hints after confirmation. It preserves unrelated files and existing extra import paths. Open **Kepoco: Open Getting Started** for the complete guide.

Snippet prefixes: kp-game, kp-sprite, kp-text, kp-rect, kp-tone, kp-save, kp-button, kp-font.

Use **Kepoco: Check IntelliSense** to exercise actual completion, hover, signature and definition providers. The check creates an editor-only fixture under examples and a JSON report under .vscode. The fixture stays outside hidden folders so Pylance can resolve its imports even when hidden paths are auto-excluded. It does not execute the Python fixture or hardware libraries.

Use **Kepoco: Open API Reference** for the generated source-signature index and **Kepoco: Open Firmware Notes** for confirmed source issues and backend caveats.

Microsoft Python and Pylance are required. Open the whole project folder, not just an individual Python file. This extension does not define a missing Python variable: use import kepoco before kepoco.display, or from kepoco import display before display.

See THIRD_PARTY_NOTICES.md and the retained source/vendor licences. Do not upload typings, vendor, or this extension to your handheld.
