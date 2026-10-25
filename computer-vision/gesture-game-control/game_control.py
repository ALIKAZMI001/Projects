"""Play a WASD game with hand gestures (the bundled Unity build is included).

Gestures
--------
* Move the cursor  — point with your index finger.
* Left click       — thumb and index tips together.
* Right click      — index and middle tips together.
* w / a / s / d    — point up / left / down / right relative to the wrist.

Run:  python game_control.py      (press 'q' to quit)

Then launch ``unity-build/TRAINING CAMP.exe`` and keep this window focused on
the game.
"""

import time

import cv2
import mediapipe as mp
import pyautogui

CLICK_THRESHOLD_PX = 40
CLICK_COOLDOWN_SECONDS = 0.5
TYPING_COOLDOWN_SECONDS = 1.0
DIRECTION_MARGIN_PX = 50


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def main() -> None:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam.")

    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()

    last_click_time = 0.0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        output = hand_detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame_height, frame_width = frame.shape[:2]

        for hand in output.multi_hand_landmarks or []:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            thumb = landmarks[4]
            index = landmarks[8]
            middle = landmarks[12]
            wrist = landmarks[0]

            thumb_x, thumb_y = int(thumb.x * frame_width), int(thumb.y * frame_height)
            index_x, index_y = int(index.x * frame_width), int(index.y * frame_height)
            middle_x, middle_y = int(middle.x * frame_width), int(middle.y * frame_height)
            wrist_x, wrist_y = int(wrist.x * frame_width), int(wrist.y * frame_height)

            pyautogui.moveTo(
                index_x * screen_width // frame_width,
                index_y * screen_height // frame_height,
            )

            now = time.time()
            if now - last_click_time > CLICK_COOLDOWN_SECONDS:
                if distance(index_x, index_y, thumb_x, thumb_y) < CLICK_THRESHOLD_PX:
                    pyautogui.click()
                    last_click_time = now
                elif distance(index_x, index_y, middle_x, middle_y) < CLICK_THRESHOLD_PX:
                    pyautogui.rightClick()
                    last_click_time = now

            if now - last_click_time > TYPING_COOLDOWN_SECONDS:
                key = None
                if index_y < wrist_y - DIRECTION_MARGIN_PX:
                    key = "w"
                elif index_y > wrist_y + DIRECTION_MARGIN_PX:
                    key = "s"
                elif index_x < wrist_x - DIRECTION_MARGIN_PX:
                    key = "a"
                elif index_x > wrist_x + DIRECTION_MARGIN_PX:
                    key = "d"

                if key:
                    pyautogui.typewrite(key)
                    last_click_time = now

            cv2.circle(frame, (index_x, index_y), 15, (255, 255, 255), cv2.FILLED)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, (middle_x, middle_y), 10, (0, 255, 255), cv2.FILLED)

        cv2.imshow("Gesture Game Control", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
