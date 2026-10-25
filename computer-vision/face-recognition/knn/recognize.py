"""Real-time face recognition with a KNN classifier over raw pixel features.

Run:  python recognize.py      (press 'q' to quit)

Requires ``data/faces_data.pkl`` and ``data/names.pkl`` — build them with
``add_faces.py``.
"""

import pickle
from pathlib import Path

import cv2
from sklearn.neighbors import KNeighborsClassifier

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CASCADE_PATH = DATA_DIR / "haarcascade_frontalface_default.xml"
FACE_SIZE = (50, 50)


def main() -> None:
    facedetect = cv2.CascadeClassifier(str(CASCADE_PATH))

    with open(DATA_DIR / "names.pkl", "rb") as f:
        labels = pickle.load(f)
    with open(DATA_DIR / "faces_data.pkl", "rb") as f:
        faces = pickle.load(f)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)

    video = cv2.VideoCapture(0)
    if not video.isOpened():
        raise SystemExit("Could not open webcam.")

    while True:
        ok, frame = video.read()
        if not ok:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for x, y, w, h in facedetect.detectMultiScale(gray, 1.3, 5):
            face = frame[y : y + h, x : x + w]
            sample = cv2.resize(face, FACE_SIZE).flatten().reshape(1, -1)
            name = knn.predict(sample)[0]

            cv2.putText(
                frame, str(name), (x, max(y - 15, 20)), cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 255, 255), 1,
            )
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

        cv2.imshow("KNN Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
