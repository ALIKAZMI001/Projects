"""Real-time webcam inference with the fine-tuned YOLOv8 face model.

Run:  python predict.py      (press 'q' to quit)
"""

from pathlib import Path

import cv2
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
WEIGHTS = BASE_DIR / "runs" / "detect" / "train" / "weights" / "best.pt"


def main() -> None:
    model = YOLO(str(WEIGHTS))
    print("Loaded classes:", model.names)
    class_names = model.names

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Failed to grab frame.")
            break

        result = model(frame, conf=0.25, verbose=False)[0]
        annotated = frame.copy()

        for box in result.boxes:
            x1, y1, x2, y2 = (int(v) for v in box.xyxy[0].tolist())
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            label = f"{class_names.get(cls_id, f'ID:{cls_id}')} {conf:.2f}"

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                annotated,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        cv2.imshow("YOLOv8 Face Detection", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
