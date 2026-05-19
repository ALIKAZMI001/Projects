import cv2
import mediapipe as mp
import time
from openpyxl import load_workbook

# Initialize webcam and mediapipe
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Load Excel workbook and select the active sheet
workbook = load_workbook('attendance.xlsx')
sheet = workbook.active
current_row = 2  # Starting from the second row (assuming first row is headers)

def calculate_distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def update_attendance(status):
    global current_row
    # Write the attendance status ('P' or 'A') in the third column
    sheet.cell(row=current_row, column=3).value = status
    # Save the workbook
    workbook.save('attendance.xlsx')

# Initial wait before starting the attendance check
print("Starting attendance check in 6 seconds...")
time.sleep(6)

while current_row <= sheet.max_row:
    student_name = sheet.cell(row=current_row, column=1).value
    print(f"Checking attendance for {student_name}")
    
    gesture_detected = False

    while not gesture_detected:
        success, frame = cap.read()
        if not success:
            break

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark

                # Extract coordinates of thumb and wrist
                thumb_tip = landmarks[4]
                wrist = landmarks[0]

                frame_height, frame_width, _ = frame.shape
                thumb_y = int(thumb_tip.y * frame_height)
                wrist_y = int(wrist.y * frame_height)

                # Check for thumb up (for present)
                if thumb_y < wrist_y - 50:
                    update_attendance('P')
                    gesture_detected = True
                    print(f"Attendance for {student_name} marked as Present")
                    time.sleep(1)  # Adding sleep to prevent multiple entries

                # Check for thumb down (for absent)
                elif thumb_y > wrist_y + 50:
                    update_attendance('A')
                    gesture_detected = True
                    print(f"Attendance for {student_name} marked as Absent")
                    time.sleep(1)  # Adding sleep to prevent multiple entries

        # Display the resulting frame
        cv2.imshow('Attendance Tracker', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            gesture_detected = True
            break

    current_row += 1

    # Wait for 12 seconds before displaying the next name
    if current_row <= sheet.max_row:
        print("Waiting for 6 seconds before the next student...")
        time.sleep(6)

cap.release()
cv2.destroyAllWindows()
print("Attendance check complete.")
