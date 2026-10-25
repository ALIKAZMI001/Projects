"""Capture face images from the webcam into ``images/<name>/``.

These images are the training set for the CNN classifier (``recognize.py``).
Run:  python collect_faces.py
"""

from pathlib import Path

import cv2

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
CASCADE = cv2.CascadeClassifier(
    str(BASE_DIR / "haarcascade_frontalface_default.xml")
)

TARGET_IMAGES = 500


def main() -> None:
    name = input("Enter your name: ").strip().lower()
    if not name:
        raise SystemExit("A name is required.")

    person_dir = IMAGES_DIR / name
    if person_dir.exists():
        print(f"'{name}' already has images in {person_dir}.")
        return
    person_dir.mkdir(parents=True)

    video = cv2.VideoCapture(0)
    if not video.isOpened():
        raise SystemExit("Could not open webcam.")

    count = 0
    while count < TARGET_IMAGES:
        ok, frame = video.read()
        if not ok:
            break

        faces = CASCADE.detectMultiScale(frame, 1.3, 5)
        for x, y, w, h in faces:
            count += 1
            out_path = person_dir / f"{count}.jpg"
            print(f"Saving {out_path}")
            cv2.imwrite(str(out_path), frame[y : y + h, x : x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow("Collecting faces", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
    print(f"Done — {count} images saved to {person_dir}")


if __name__ == "__main__":
    main()
