import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize webcam and mediapipe
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Initialize variables
index_x, index_y = 0, 0
click_threshold = 40  # Distance threshold for click actions
last_click_time = 0
click_cooldown = 0.5  # Cooldown time in seconds
typing_cooldown = 1  # Cooldown time for typing gestures

def calculate_distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# Loop to read frames from webcam
while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            # Extract coordinates of thumb, index, and middle tips
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            middle_tip = landmarks[12]
            wrist = landmarks[0]  # Palm base or wrist

            frame_height, frame_width, _ = frame.shape
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)
            index_x = int(index_tip.x * frame_width)
            index_y = int(index_tip.y * frame_height)
            middle_x = int(middle_tip.x * frame_width)
            middle_y = int(middle_tip.y * frame_height)
            wrist_x = int(wrist.x * frame_width)
            wrist_y = int(wrist.y * frame_height)

            # Move the mouse cursor
            pyautogui.moveTo(index_x * screen_width // frame_width, index_y * screen_height // frame_height)

            current_time = time.time()

            # Calculate distances
            thumb_index_dist = calculate_distance(index_x, index_y, thumb_x, thumb_y)
            index_middle_dist = calculate_distance(index_x, index_y, middle_x, middle_y)

            # Check for left click (index and thumb tips close together)
            if thumb_index_dist < click_threshold:
                if current_time - last_click_time > click_cooldown:
                    pyautogui.click()
                    last_click_time = current_time

            # Check for right click (index and middle tips close together)
            if index_middle_dist < click_threshold:
                if current_time - last_click_time > click_cooldown:
                    pyautogui.rightClick()
                    last_click_time = current_time

            # Determine direction for typing
            if current_time - last_click_time > typing_cooldown:
                if index_y < wrist_y - 50:  # Finger pointing up
                    pyautogui.typewrite('w')
                    last_click_time = current_time
                elif index_y > wrist_y + 50:  # Finger pointing down
                    pyautogui.typewrite('s')
                    last_click_time = current_time
                elif index_x < wrist_x - 50:  # Finger pointing left
                    pyautogui.typewrite('a')
                    last_click_time = current_time
                elif index_x > wrist_x + 50:  # Finger pointing right
                    pyautogui.typewrite('d')
                    last_click_time = current_time

            # Draw circles on landmarks
            cv2.circle(frame, (index_x, index_y), 15, (255, 255, 255), cv2.FILLED)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, (middle_x, middle_y), 10, (0, 255, 255), cv2.FILLED)

    # Display the resulting frame
    cv2.imshow('Virtual Mouse', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
