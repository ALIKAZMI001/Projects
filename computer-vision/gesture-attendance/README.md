# Gesture Attendance

Marks a class register using hand gestures instead of a keyboard. The script walks
down `attendance.xlsx` one student at a time and waits for a gesture:

| Gesture | Meaning | Written to column C |
| --- | --- | --- |
| 👍 thumb above the wrist | Present | `P` |
| 👎 thumb below the wrist | Absent | `A` |

Press `q` to skip the current student.

## How it works

1. Load the workbook and start at row 2 (row 1 is the header).
2. For each student, read webcam frames and run MediaPipe Hands.
3. Compare the thumb-tip and wrist y-coordinates: a margin of 50 px decides
   up vs. down.
4. Write `P`/`A`, save the workbook, and move to the next student.

The gesture is detected relative to the wrist rather than an absolute position, so
it works at different distances from the camera. A short cooldown after each write
prevents a held gesture from being recorded twice.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python attendance.py
```

## Register format

`attendance.xlsx` — column A is the student name, column C receives the mark:

| A | B | C |
| --- | --- | --- |
| Name | Roll No | Attendance |
| Ali | 01 | |
| Sara | 02 | |

Swap in your own file with the same shape and the script works unchanged.

## Stack

`mediapipe` · `opencv-python` · `openpyxl`
