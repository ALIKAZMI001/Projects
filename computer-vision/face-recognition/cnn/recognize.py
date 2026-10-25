"""Real-time face recognition with a Keras classifier (Teachable-Machine style).

Run:  python recognize.py      (press 'q' to quit)

The class order must match how ``keras_model.h5`` was trained. Edit
``CLASS_NAMES`` if you retrain with a different label set.
"""

from pathlib import Path

import cv2
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent
CASCADE_PATH = BASE_DIR / "haarcascade_frontalface_default.xml"
MODEL_PATH = BASE_DIR / "keras_model.h5"

CLASS_NAMES = {0: "Ali", 1: "Other Person"}
FONT = cv2.FONT_HERSHEY_COMPLEX
INPUT_SIZE = 224


def classify(model, face_bgr: np.ndarray) -> tuple[str, float]:
    img = cv2.resize(face_bgr, (INPUT_SIZE, INPUT_SIZE))
    img = img.reshape(1, INPUT_SIZE, INPUT_SIZE, 3).astype(np.float32) / 255.0

    prediction = model.predict(img, verbose=0)
    class_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))
    return CLASS_NAMES.get(class_index, "Unknown"), confidence


def main() -> None:
    facedetect = cv2.CascadeClassifier(str(CASCADE_PATH))
    model = load_model(MODEL_PATH, compile=False)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam.")
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        for x, y, w, h in facedetect.detectMultiScale(frame, 1.3, 5):
            label, confidence = classify(model, frame[y : y + h, x : x + w])

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (0, 255, 0), -2)
            cv2.putText(
                frame, label, (x + 5, y - 10), FONT, 0.75, (255, 255, 255), 1, cv2.LINE_AA
            )
            cv2.putText(
                frame,
                f"{confidence * 100:.2f}%",
                (x, y + h + 20),
                FONT,
                0.75,
                (255, 0, 0),
                2,
                cv2.LINE_AA,
            )

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
