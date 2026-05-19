import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load model
model = load_model(r'D:\1\2\PROJECT\AGE.GENDER\imdb_crop\age_gender_model.h5', compile=False)

gender_labels = ['Female', 'Male']
IMG_SIZE = 128

def preprocess(image):
    img = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    input_img = preprocess(frame)
    gender_pred, age_pred = model.predict(input_img, verbose=0)

    gender_idx = np.argmax(gender_pred[0])
    gender_text = gender_labels[gender_idx]
    age_val = age_pred[0][0]
    age_text = f"{age_val:.1f} years"

    # Draw predictions
    cv2.putText(frame, f"Gender: {gender_text}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Age: {age_text}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Live Age and Gender Prediction', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
