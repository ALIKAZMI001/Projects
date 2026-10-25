# Virtual Mouse

Controls the operating-system cursor with hand landmarks from the webcam — no
mouse, no touchpad.

| Gesture | Action |
| --- | --- |
| Index finger pointing | Cursor follows the fingertip |
| Thumb + index tips together | Left click |
| Index + middle tips together | Right click |

Press `q` to quit. `PyAutoGUI`'s fail-safe is active: slam the real mouse into a
screen corner to abort.

## Implementation notes

- The frame is mirrored (`cv2.flip`) so movement feels natural, and MediaPipe runs
  on the RGB copy.
- Fingertip coordinates are normalised by frame size and then scaled to the screen
  resolution, so the cursor reaches the full desktop regardless of webcam aspect
  ratio.
- An **exponential smoothing** filter (`SMOOTHING = 0.5`) on the cursor position
  removes the frame-to-frame jitter you get from raw landmarks while staying
  responsive.
- Clicks are debounced with a 0.5 s cooldown, and the left-click check runs before
  the right-click one so a pinch can't fire both.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python virtual_mouse.py
```

## Tuning

| Constant | Default | Effect |
| --- | --- | --- |
| `CLICK_THRESHOLD_PX` | 40 | How close fingertips must be to register a click |
| `CLICK_COOLDOWN_SECONDS` | 0.5 | Minimum gap between clicks |
| `SMOOTHING` | 0.5 | Higher = smoother but laggier cursor |

## Stack

`mediapipe` · `opencv-python` · `pyautogui`
