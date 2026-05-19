import cv2
from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO("runs/detect/train/weights/best.pt")
print("✅ Loaded class names:", model.names)
class_names = model.names

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame.")
        break

    # Run inference
    results = model(frame, conf=0.25)[0]  # Get first result directly
    print(f"📦 Boxes in frame: {len(results.boxes)}")

    annotated_frame = frame.copy()

    if results.boxes and len(results.boxes) > 0:
        for box in results.boxes:
            # Safely extract values
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            name = class_names.get(cls_id, f"ID:{cls_id}")

            # Draw bounding box
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label
            label = f"{name} {conf:.2f}"
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        print("😐 No valid boxes found.")

    # Display annotated frame
    cv2.imshow("YOLOv8 Face Recognition", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
