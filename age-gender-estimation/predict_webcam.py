"""Live webcam age + gender prediction using the joint two-head CNN.

Run:  python predict_webcam.py      (press 'q' to quit)
"""

from pathlib import Path

import cv2
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "age_gender_model.h5"

IMG_SIZE = 128
GENDER_LABELS = ["Female", "Male"]
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def preprocess(face_bgr: np.ndarray) -> np.ndarray:
    img = cv2.resize(face_bgr, (IMG_SIZE, IMG_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)


def main() -> None:
    model = load_model(MODEL_PATH, compile=False)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for x, y, w, h in faces:
            face = frame[y : y + h, x : x + w]
            if face.size == 0:
                continue

            gender_pred, age_pred = model.predict(preprocess(face), verbose=0)
            gender = GENDER_LABELS[int(np.argmax(gender_pred[0]))]
            age = float(age_pred[0][0])

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{gender}, {age:.0f} yrs",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

        cv2.imshow("Age & Gender Estimation", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
