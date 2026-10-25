"""Control the mouse cursor with hand gestures through the webcam.

Gestures
--------
* Move the cursor  — point with your index finger.
* Left click       — bring thumb and index tips together.
* Right click      — bring index and middle tips together.

Run:  python virtual_mouse.py      (press 'q' to quit)

Safety: the cursor is driven by ``pyautogui``, so set ``pyautogui.FAILSAFE``
behaviour in mind — slam the mouse into a screen corner to abort.
"""

import time

import cv2
import mediapipe as mp
import pyautogui

CLICK_THRESHOLD_PX = 40
CLICK_COOLDOWN_SECONDS = 0.5
SMOOTHING = 0.5  # 0 = no smoothing, 1 = frozen; 0.5 removes most jitter


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
    prev_x = prev_y = None

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

            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            middle_tip = landmarks[12]

            thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
            index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
            middle_x, middle_y = int(middle_tip.x * frame_width), int(middle_tip.y * frame_height)

            target_x = index_x * screen_width // frame_width
            target_y = index_y * screen_height // frame_height

            # Exponential smoothing keeps the cursor from twitching.
            if prev_x is None:
                prev_x, prev_y = target_x, target_y
            prev_x = int(SMOOTHING * prev_x + (1 - SMOOTHING) * target_x)
            prev_y = int(SMOOTHING * prev_y + (1 - SMOOTHING) * target_y)
            pyautogui.moveTo(prev_x, prev_y)

            now = time.time()
            if now - last_click_time > CLICK_COOLDOWN_SECONDS:
                if distance(index_x, index_y, thumb_x, thumb_y) < CLICK_THRESHOLD_PX:
                    pyautogui.click()
                    last_click_time = now
                elif distance(index_x, index_y, middle_x, middle_y) < CLICK_THRESHOLD_PX:
                    pyautogui.rightClick()
                    last_click_time = now

            cv2.circle(frame, (index_x, index_y), 15, (255, 255, 255), cv2.FILLED)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, (middle_x, middle_y), 10, (0, 255, 255), cv2.FILLED)

        cv2.imshow("Virtual Mouse", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
