import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from keras.models import load_model

# Load Haar Cascade for face detection
facedetect = cv2.CascadeClassifier(
    r'D:\1\2\PROJECT\Projects Internship\FACE RECOGNITION USING MACHINE LEARNING TECHNIQUES\Cnn\haarcascade_frontalface_default.xml'
)

# Open the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Set font for text
font = cv2.FONT_HERSHEY_COMPLEX

# Load the pre-trained model
model = load_model(
    r'D:\1\2\PROJECT\Projects Internship\FACE RECOGNITION USING MACHINE LEARNING TECHNIQUES\Cnn\keras_model.h5'
)

# Function to map class index to name
def get_className(classNo):
    if classNo == 0:
        return "Ali"
    elif classNo == 1:
        return "Other Person"
    else:
        return "Unknown"

# Main loop
while True:
    success, imgOriginal = cap.read()
    faces = facedetect.detectMultiScale(imgOriginal, 1.3, 5)

    for x, y, w, h in faces:
        crop_img = imgOriginal[y:y+h, x:x+w]
        img = cv2.resize(crop_img, (224, 224))
        img = img.reshape(1, 224, 224, 3)
        img = img.astype(np.float32) / 255.0  # Normalize if model expects it

        prediction = model.predict(img)
        classIndex = np.argmax(prediction)
        probabilityValue = np.amax(prediction)

        # Draw bounding box and label
        cv2.rectangle(imgOriginal, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.rectangle(imgOriginal, (x, y - 40), (x + w, y), (0, 255, 0), -2)
        cv2.putText(
            imgOriginal,
            f"{get_className(classIndex)}",
            (x, y - 10),
            font,
            0.75,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        # Show probability
        cv2.putText(
            imgOriginal,
            str(round(probabilityValue * 100, 2)) + "%",
            (x, y + h + 20),
            font,
            0.75,
            (255, 0, 0),
            2,
            cv2.LINE_AA
        )

    # Show the frame
    cv2.imshow("Result", imgOriginal)

    # Quit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
