"""Capture a new person's faces and append them to the KNN training data.

Run:  python add_faces.py [name]

Writes ``images/<name>/*.jpg`` plus the flattened face vectors into
``data/faces_data.pkl`` and the matching labels into ``data/names.pkl``.
"""

import pickle
import sys
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
DATA_DIR = BASE_DIR / "data"
CASCADE_PATH = DATA_DIR / "haarcascade_frontalface_default.xml"

TARGET_IMAGES = 100
FACE_SIZE = (50, 50)


def get_name() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1].strip().lower()
    return input("Enter your name: ").strip().lower()


def main() -> None:
    name = get_name()
    if not name:
        raise SystemExit("A name is required.")

    person_dir = IMAGES_DIR / name
    if person_dir.exists():
        print(f"'{name}' already exists — use a different name.")
        raise SystemExit(1)
    person_dir.mkdir(parents=True)

    facedetect = cv2.CascadeClassifier(str(CASCADE_PATH))
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        raise SystemExit("Could not open webcam.")

    faces_data: list[np.ndarray] = []
    count = 0

    while count < TARGET_IMAGES:
        ok, frame = video.read()
        if not ok:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for x, y, w, h in facedetect.detectMultiScale(gray, 1.3, 5):
            count += 1
            face = frame[y : y + h, x : x + w]
            image_path = person_dir / f"{count}.jpg"
            print(f"Creating {image_path}")
            cv2.imwrite(str(image_path), face)

            faces_data.append(cv2.resize(face, FACE_SIZE))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow("Adding faces", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()

    if not faces_data:
        raise SystemExit("No faces captured — nothing saved.")

    faces_array = np.asarray(faces_data).reshape(len(faces_data), -1)
    DATA_DIR.mkdir(exist_ok=True)

    names_file = DATA_DIR / "names.pkl"
    if names_file.exists():
        with open(names_file, "rb") as f:
            names = pickle.load(f)
    else:
        names = []
    names += [name] * len(faces_array)
    with open(names_file, "wb") as f:
        pickle.dump(names, f)

    faces_file = DATA_DIR / "faces_data.pkl"
    if faces_file.exists():
        with open(faces_file, "rb") as f:
            faces_array = np.append(pickle.load(f), faces_array, axis=0)
    with open(faces_file, "wb") as f:
        pickle.dump(faces_array, f)

    print(f"Saved {len(faces_data)} faces for '{name}'.")


if __name__ == "__main__":
    main()
