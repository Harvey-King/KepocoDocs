# Save and test from VS Code over USB

[Overview](readme.md) · [Getting started](GETTING_STARTED.md) · [Features](FEATURE_GUIDE.md) · [API reference](API_REFERENCE.md) · [Firmware notes](FIRMWARE_NOTES.md) · [USB workflow](USB_WORKFLOW.md)

Run and upload **single-file games** using the repository’s VS Code tasks and `tools/usb_device.py`. These tools use the firmware already installed on the handheld; they do not flash firmware or install the archived `source-library/` files.

## Prepare the local checkout

Open the root of your local KepocoDocs checkout in VS Code. You need desktop Python with `venv` support, a USB data cable, and a handheld with a working Kepoco MicroPython runtime. Create the environment from the checkout root:

```sh
python -m venv .venv
```

Then install the development requirements using **that environment’s interpreter** (activation is not required).

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

**macOS/Linux:**

```sh
.venv/bin/python -m pip install -r requirements-dev.txt
```

The tasks in `.vscode/tasks.json` call `tools/usb_device.py` with `.venv/Scripts/python` on Windows or `.venv/bin/python` on macOS/Linux. Do not copy an interpreter path from someone else’s PC. The runner invokes `mpremote` through the same Python interpreter.

The VSIX is installed separately using **Extensions: Install from VSIX**; see the [overview](readme.md). It provides editor support, not a USB task installer. Extension project setup alone does **not** supply this runner, the tasks, or their Python dependencies. Keep the repository’s tools and task configuration in your checkout.

## Quick test

1. Disconnect the handheld from the web editor or other USB console; only one program can own its serial port.
2. Open your game’s `.py` file in VS Code.
3. Press **Ctrl+S** to save it.
4. Press **Ctrl+Shift+B**. The default build task is **Kepoco: Run current file on USB**.
5. Test on the handheld. Python output and tracebacks appear in the task terminal.

The runner soft-resets the target, then sends and executes the saved local file with `mpremote run`. This does **not** install the file permanently. The desktop Python Run button is a different operation and cannot run the firmware’s `kepoco` module.

For SWERVE: A starts/retries; left/right steer; hold A to boost; B exits (`swerve.py:183–191`). These are the game’s intended controls, not a claim of human control testing. Save before every test; the runner uses the file on disk.

## Device selection

The runner defaults to **`auto`**. If you have multiple serial devices connected, select the intended handheld explicitly. For example, on Windows:

```powershell
.\.venv\Scripts\python.exe tools/usb_device.py info --device COM7
.\.venv\Scripts\python.exe tools/usb_device.py run swerve.py --device COM7
```

`COM7` is an example, not a required port. On macOS/Linux, use `.venv/bin/python` and your device’s port. A user-supplied USB serial selector is also optional: pass `--device "id:<your-USB-serial>"`, replacing the placeholder with your own device identity. No private device identity is bundled in these instructions.

List available connections with your environment’s Python:

```sh
.venv/bin/python -m mpremote connect list
```

On Windows, use `.\.venv\Scripts\python.exe -m mpremote connect list` instead. If adding an explicit selector to a VS Code task, put `--device` and your selector in its `args` array; leave the portable interpreter command intact.

## Save the game onto the handheld

Use **Terminal > Run Task > Kepoco: Upload current game to handheld** after saving the game.

The task creates `/Games/<filename-without-extension>/<filename>.py`, copies that one file, then reads the exact destination on the device and computes its SHA-256. The returned hash must match the saved local file's SHA-256. For `swerve.py`, the destination is `/Games/swerve/swerve.py`. A subsequent upload replaces that game file. Do not treat an upload as verified unless this remote-content comparison succeeds; the task does not download the whole file back to the PC.

This task is for single-file games only. Do not upload `typings/`, documentation, `source-library/`, vendor files, firmware modules, `boot.py` or `main.py`. Assets and helper modules require their own reviewed deployment; this task does not deploy them.

After upload, use **Kepoco: Return to device menu**, or reconnect/reboot the handheld. Installation in `/Games` does not by itself prove whether or how the firmware menu lists the game; automatic menu registration has not been visually verified.

## Other tasks

- **Kepoco: Device information** — firmware identification and Games listing.
- **Kepoco: USB console (REPL)** — interactive MicroPython prompt; Ctrl+] exits mpremote’s REPL.
- **Kepoco: Return to device menu** — hardware reset into the existing firmware startup; visible menu behavior is a separate check.

## Troubleshooting

- **Port busy:** disconnect the web editor and stop other USB console/game tasks. Use VS Code’s task terminal controls to terminate a task that owns the port; reconnect USB if needed. Do not kill unrelated processes.
- **Task cannot find Python or mpremote:** create `.venv` at the checkout root and install `requirements-dev.txt` with the appropriate environment interpreter shown above.
- **Wrong device or no connection:** check the cable and connection listing, then use an explicit selector for your handheld.
- **A game task stays active:** it runs until the game exits or is interrupted. Stop it before launching another USB task.
- **Runtime exception:** capture the exact traceback and firmware identification. [Firmware notes](FIRMWARE_NOTES.md) describe archive defects, which do not necessarily match your installed runtime.

Do not use BOOTSEL for normal game upload/testing. These tasks do not repair runtime libraries or flash a replacement firmware.

## Prior real-device verification

The following was verified previously on a connected handheld, not repeated by this documentation update:

- Retrieved firmware identification: **MicroPython 1.29.0, KEPOCO build**, plus root/Games directory listings.
- Uploaded `swerve.py` and verified the remote file against the saved local contents by read-back.
- Imported the uploaded game and installed Kepoco runtime.
- Executed **60 gameplay frames** on the actual display driver without an exception.
- Executed title, gameplay and crash drawing; the display reported **72×40**.

This is real device execution, not host simulation or human visual acceptance. Physical controls, visible image quality, long-session playability and automatic menu registration still need human testing. The archived library was **not** installed; the existing device runtime was used. No firmware was flashed or startup files changed. See [the archive audit](FIRMWARE_NOTES.md) for its separate scope and source citations.

Reference: [MicroPython mpremote documentation](https://docs.micropython.org/en/latest/reference/mpremote.html).
