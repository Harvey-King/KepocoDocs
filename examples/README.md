# Kepoco example cookbook

[Repository overview](../readme.md) · [Setup](../GETTING_STARTED.md) · [USB run/upload](../USB_WORKFLOW.md) · [API reference](../API_REFERENCE.md)

Start with the menu example, then try the four lessons below. Each `.py` file is a complete, independent program: no helper files need uploading. Open it in the repository workspace, save with **Ctrl+S**, then **Ctrl+Shift+B** to run the saved file on your connected Kepoco. Disconnect the web editor first. The desktop Python Run button is not a handheld runner.

## Example list

| Order | Example | What it teaches | Controls |
|---|---|---|---|
| 1 | [Menu, settings and slider](02_menu_settings_slider.py) | Screen states, menu selection, changing a real variable and using it in gameplay | U/D select, A open, L/R adjust, B back/exit |
| 2 | [Smooth movement](03_smooth_movement.py) | Held buttons, elapsed-time movement, clamping to the screen | D-pad move, B exit |
| 3 | [Animated sprite](04_animated_sprite.py) | Bitmap bytes, multiple frames and timed animation | L/R move, A pause/resume, B exit |
| 4 | [Collect the dot](05_collect_the_dot.py) | Rectangle collision, score and safe respawning | D-pad move, A reset, B exit |
| 5 | [Stopwatch](06_stopwatch.py) | Start/pause/reset and wrap-safe tick arithmetic | A start/pause, L reset, B exit |

Also available: [minimal steering starter](01_quickstart.py) and the complete [SWERVE game](../swerve.py).

## 1. Menu → settings → slider → gameplay

Run [02_menu_settings_slider.py](02_menu_settings_slider.py). The first screen offers Play, Settings and Quit. Up/Down moves the selection; A opens the selected item. Open Settings, change the speed with Left/Right, then press B to return and choose Play. The moving square uses the speed you just selected. B returns from Play to the menu; B on the menu exits.

The important distinction is **the value versus its picture**. The speed is an integer in program state; the slider is only a drawing of that integer. Moving the knob without changing the speed would not change gameplay.

The update is conceptually:

```python
# +1 for right, -1 for left, 0 when neither/both is pressed.
speed = max(minimum, min(maximum, speed + direction * step))
```

For this lesson the bounds are 0–100 and the step is 5. The initial speed is 40 (`START_SPEED`). Edit the starting-value constant to change the default; edit the step constant to make each press change it more or less. The bound check prevents selecting negative speed or exceeding the maximum. At zero the square stops.

The drawing maps the value into a pixel position:

```python
fraction = (speed - minimum) / (maximum - minimum)
knob_x = track_left + int(fraction * usable_track_width)
```

Keep maximum greater than minimum. `usable_track_width` reserves enough room for the knob itself, so it remains inside the bar. These snippets explain the idea; the complete file supplies all state, bounds, drawing and controls.

Gameplay then uses that value rather than the knob position:

```python
x += speed * elapsed_ms / 1000
```

That means speed is **pixels per second**, not pixels per frame. The program uses `ticks_diff()` for elapsed time and limits a long frame so a temporary stall does not cause a giant jump. Menu choices use `justPressed()` so one press means one choice change; the edge methods are read once per frame.

Settings survive going between these screens, but only **in RAM**. Restarting the program restores its default. This example does not write a settings file, change device brightness or overwrite firmware.

## 2. Smooth four-direction movement

[03_smooth_movement.py](03_smooth_movement.py) is the small foundation for a player character. It reads held D-pad input with `pressed()`, computes elapsed milliseconds, moves the square and clamps it into the visible playfield.

Why elapsed time? Adding a fixed number every frame makes speed depend on delivered frame rate. Multiplying pixels-per-second by elapsed seconds keeps movement steadier. `setFPS(30)` is a frame cap, not a measurement that exactly 30 frames were delivered. A long-frame cap protects against pauses or USB/debugging stalls.

Try changing the `30` pixels-per-second multiplier in the movement calculations and the square's `4`-pixel size. If you change the size, also update the `68` right-edge bound and the `27` bottom-edge bound to keep the whole square inside the playfield. In a reusable game, derive those limits from the display/playfield dimensions **minus the square size**. Held input belongs in movement; an edge event belongs in menu selection.

## 3. Animated bitmap sprite

[04_animated_sprite.py](04_animated_sprite.py) builds a real `kepoco.Sprite`, moves it with Left/Right and switches between bitmap frames on a timer. A pauses/resumes the animation; B exits.

For an **8×8** monochrome sprite, one frame needs eight bytes. Each byte describes one vertical column: bit 0 is the top pixel, bit 7 is the bottom. Two frames go in one `bytearray` of 16 bytes, with frame 0's eight bytes followed by frame 1's eight bytes. Do not pass a list of two frame arrays: the source treats a two-array tuple/list as grayscale bitplanes, not an animation frame list.

`setFrame(frame_number)` selects the current frame; `display.drawSprite(sprite)` draws it. Changing `sprite.x` moves the image without editing its bitmap. The example uses a transparent-black key so only the sprite's lit pixels cover the background. Edit the bitmap bytes to draw your own character, or change the animation interval to speed up the animation.

The exact constructor and frame rules are evidenced by `source-library/thumbySprite.py:26–102`. Bigger images require more bytes: width × the number of eight-pixel-high pages per frame.

## 4. Collect-the-dot mini-game

[05_collect_the_dot.py](05_collect_the_dot.py) turns movement into a small game. Move the player onto a target to score; the target is then placed somewhere new. A resets the game; B exits.

Collision is checked against the two rectangles, not by asking the framebuffer which pixels were drawn:

```python
hit = (player_x < target_x + target_width
       and player_x + player_width > target_x
       and player_y < target_y + target_height
       and player_y + player_height > target_y)
```

All four comparisons must be true. Touching an edge without overlapping does not count. The target's whole rectangle must remain inside the playfield, and a new target must not already overlap the player—otherwise you could score again without moving. The example keeps score and drawing separate, so you can change the graphics without changing collision logic.

Try making the target smaller, moving the player faster, or adding a countdown using the stopwatch lesson. Avoid `getPixel()` for collision: the archived Kepoco wrapper does not return the driver's pixel value.

## 5. Stopwatch with start/pause/reset

[06_stopwatch.py](06_stopwatch.py) tracks elapsed time without blocking the frame loop. A starts or pauses it, Left resets the elapsed value **and pauses**, and B exits. Reset takes priority if A and Left are pressed together. Controls remain responsive while time is being displayed.

A tick counter eventually wraps, so use `time.ticks_diff(now, previous)` rather than plain `now - previous`. Accumulate differences while running; while paused, keep updating the reference tick without adding paused time. That prevents a large jump when resuming. Tick differences still require regularly sampling the clock within the runtime's valid tick-difference interval; the frame loop does that.

The display formats elapsed milliseconds into a compact clock with tenths of a second. This example stops and holds at **99:59.9** so the label stays inside the screen; it does not silently roll back to zero. That limit is `5999900` milliseconds in the script. This pattern also works for cooldowns, round timers and animation clocks. It measures runtime ticks, not wall-clock/calendar time.

## Runtime and verification boundaries

These examples target the existing Kepoco firmware, a 72×40 screen, the six named gamepad buttons and `/lib/font5x7.bin`. Labels use ASCII `bytes` (dynamic labels are encoded) because the archived `drawText()` implementation reads `memoryview(text)`; ordinary Python strings are not safe on that implementation. Exact graphics/text methods are documented in the [API reference](../API_REFERENCE.md), and known backend issues in [firmware notes](../FIRMWARE_NOTES.md).

Host tests exercise the real example logic with fake buttons, graphics and a tick clock. Those tests are not a desktop emulator or proof of physical controls/rendering. Passing static checks does not fix an installed firmware incompatibility. The scripts provide `main(max_frames=...)` for a bounded smoke run; ordinary `main()` runs interactively until exit. No example flashes firmware or writes persistent settings.

If a runtime error occurs, report the exact traceback and firmware identification. Keep editor stubs and `source-library` on the PC; upload only the individual example `.py` file through the guarded USB task.
