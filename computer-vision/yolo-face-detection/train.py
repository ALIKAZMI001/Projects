"""Collect a custom face dataset with MediaPipe, then fine-tune YOLOv8n on it.

Workflow
--------
1. Ask for a person's name, capture 200 face crops from the webcam and write a
   YOLO label (full-box) for each.
2. Split 75% train / 25% validation per person.
3. Regenerate ``data.yaml``.
4. Fine-tune ``yolov8n.pt`` for 10 epochs.

Run:  python train.py
"""

import shutil
from pathlib import Path

import cv2
import mediapipe as mp
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
IMG_TRAIN = DATASET_DIR / "images" / "train"
IMG_VAL = DATASET_DIR / "images" / "val"
LABEL_TRAIN = DATASET_DIR / "labels" / "train"
LABEL_VAL = DATASET_DIR / "labels" / "val"

IMAGES_PER_PERSON = 200
TRAIN_SPLIT = 0.75
EPOCHS = 10
IMG_SIZE = 640


def collect_dataset() -> list[str]:
    """Capture face crops for one or more people and return their class names."""
    for directory in (IMG_TRAIN, IMG_VAL, LABEL_TRAIN, LABEL_VAL):
        directory.mkdir(parents=True, exist_ok=True)

    detector = mp.solutions.face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5
    )
    names: list[str] = []

    while True:
        name = input("\nEnter person's name (or 'done' to finish): ").strip()
        if name.lower() == "done":
            break
        if not name:
            continue
        if name in names:
            print("Name already added. Skipping.")
            continue

        class_id = len(names)
        names.append(name)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise SystemExit("Could not open webcam.")

        count = 0
        print(f"\nCapturing {IMAGES_PER_PERSON} face images for '{name}' "
              f"(class {class_id}). Press 'q' to stop early.")

        while count < IMAGES_PER_PERSON:
            ok, frame = cap.read()
            if not ok:
                break

            h, w = frame.shape[:2]
            result = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if result.detections:
                for det in result.detections:
                    box = det.location_data.relative_bounding_box
                    x = max(0, int(box.xmin * w))
                    y = max(0, int(box.ymin * h))
                    bw = min(int(box.width * w), w - x)
                    bh = min(int(box.height * h), h - y)

                    face = frame[y : y + bh, x : x + bw]
                    if face.size == 0:
                        continue

                    cv2.imwrite(str(IMG_TRAIN / f"{name}_{count}.jpg"), face)
                    # The crop is the whole image, so the box is the full frame.
                    (LABEL_TRAIN / f"{name}_{count}.txt").write_text(
                        f"{class_id} 0.5 0.5 1.0 1.0\n", encoding="utf-8"
                    )
                    print(f"[{count + 1}/{IMAGES_PER_PERSON}] saved")
                    count += 1
                    break

            cv2.imshow(f"Capturing: {name}", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Early stop.")
                break

        cap.release()
        cv2.destroyAllWindows()

    return names


def split_train_val(names: list[str]) -> None:
    """Move the tail of each person's images/labels into the validation split."""
    print("\nSplitting train/val...")
    for name in names:
        files = sorted(f for f in IMG_TRAIN.iterdir() if f.name.startswith(name))
        split_index = int(len(files) * TRAIN_SPLIT)

        for img_path in files[split_index:]:
            shutil.move(str(img_path), str(IMG_VAL / img_path.name))
            label_path = LABEL_TRAIN / f"{img_path.stem}.txt"
            if label_path.exists():
                shutil.move(str(label_path), str(LABEL_VAL / label_path.name))


def write_data_yaml(names: list[str]) -> Path:
    yaml_path = BASE_DIR / "data.yaml"
    yaml_path.write_text(
        "path: dataset\n"
        "train: images/train\n"
        "val: images/val\n"
        f"nc: {len(names)}\n"
        f"names: {names}\n",
        encoding="utf-8",
    )
    return yaml_path


def main() -> None:
    names = collect_dataset()
    if not names:
        raise SystemExit("No names collected — nothing to train on.")

    split_train_val(names)
    yaml_path = write_data_yaml(names)
    print(f"Dataset ready, config written to {yaml_path.name}. Starting training...")

    last_weights = BASE_DIR / "runs" / "detect" / "train" / "weights" / "last.pt"
    if last_weights.exists():
        print("Resuming from the previous checkpoint...")
        model = YOLO(str(last_weights))
    else:
        print("Training from yolov8n.pt...")
        model = YOLO("yolov8n.pt")

    model.train(data=str(yaml_path), epochs=EPOCHS, imgsz=IMG_SIZE)
    print("Done. Run predict.py for live detection.")


if __name__ == "__main__":
    main()
