# Gesture Game Control

Plays a Unity shooting game with hand gestures. The Python script translates
landmarks into mouse movement, clicks and WASD keystrokes; the game itself is a
small Unity build included in `unity-build/`.

| Gesture | Action |
| --- | --- |
| Index finger pointing | Aim (moves the cursor) |
| Thumb + index tips together | Left click / shoot |
| Index + middle tips together | Right click |
| Index above the wrist | `w` |
| Index below the wrist | `s` |
| Index left of the wrist | `a` |
| Index right of the wrist | `d` |

## Run

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python game_control.py
```

Then start `unity-build/TRAINING CAMP.exe` and keep the Python preview window
focused on the game window.

## Layout

```
gesture-game-control/
├── game_control.py     # gesture → mouse + keyboard bridge
└── unity-build/        # standalone Unity player (Windows x64)
```

## Implementation notes

- Direction keys are derived from the **index fingertip relative to the wrist**, not
  from absolute screen position — so the same gesture works wherever your hand is.
- Two independent cooldowns: 0.5 s for clicks and 1 s for movement keys, which keeps
  a held gesture from spamming keystrokes.
- Click detection is checked before movement, so a pinch always registers as a click.
- The Unity build is committed so the demo is reproducible end-to-end.

## Stack

`mediapipe` · `opencv-python` · `pyautogui` · Unity
