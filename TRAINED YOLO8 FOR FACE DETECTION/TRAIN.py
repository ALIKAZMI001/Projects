import cv2
import os
import shutil
import mediapipe as mp
from ultralytics import YOLO

# === SETUP ===
base_path = os.path.dirname(os.path.abspath(__file__))
img_train = os.path.join(base_path, "dataset/images/train")
img_val = os.path.join(base_path, "dataset/images/val")
label_train = os.path.join(base_path, "dataset/labels/train")
label_val = os.path.join(base_path, "dataset/labels/val")

for d in [img_train, img_val, label_train, label_val]:
    os.makedirs(d, exist_ok=True)

mp_face = mp.solutions.face_detection
detector = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

names = []

# === DATA COLLECTION ===
while True:
    your_name = input("\nEnter person's name (or 'done' to finish): ").strip()

    if your_name.lower() == 'done':
        break

    if your_name in names:
        print("⚠️ Name already added. Skipping.")
        continue

    class_id = len(names)
    names.append(your_name)

    cap = cv2.VideoCapture(0)
    count = 0
    total_images = 200
    print(f"\n📸 Capturing 200 face images for '{your_name}' (ID {class_id})... Press 'q' to stop early.\n")

    while count < total_images:
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = detector.process(rgb)

        if result.detections:
            for det in result.detections:
                bbox = det.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                x = max(0, x)
                y = max(0, y)
                width = min(width, w - x)
                height = min(height, h - y)

                # Crop and save face
                face_img = frame[y:y+height, x:x+width]
                if face_img.size == 0:
                    continue

                img_path = os.path.join(img_train, f"{your_name}_{count}.jpg")
                txt_path = os.path.join(label_train, f"{your_name}_{count}.txt")
                cv2.imwrite(img_path, face_img)

                # Write full-box label for cropped image
                with open(txt_path, "w") as f:
                    f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

                print(f"[{count+1}/200] Saved: {img_path}")
                count += 1
                break

        cv2.imshow(f"Capturing: {your_name}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("❗ Early stop.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Finished for {your_name}.")

# === SPLIT TRAIN/VAL ===
print("\n📂 Splitting 75% train / 25% val...")
for name in names:
    files = [f for f in os.listdir(img_train) if f.startswith(name)]
    files.sort()
    split_index = int(len(files) * 0.75)

    for f in files[split_index:]:
        # Move image
        shutil.move(os.path.join(img_train, f), os.path.join(img_val, f))
        # Move label
        txt_file = f.replace(".jpg", ".txt")
        shutil.move(os.path.join(label_train, txt_file), os.path.join(label_val, txt_file))

# === Write data.yaml ===
yaml_path = os.path.join(base_path, "data.yaml")
with open(yaml_path, "w") as f:
    f.write(f"""
path: dataset
train: images/train
val: images/val
nc: {len(names)}
names: {names}
""".strip())

print("\n✅ Dataset ready. Starting YOLOv8 training...")

# === Train ===
weights_path = os.path.join(base_path, "runs/detect/train/weights/last.pt")
if os.path.exists(weights_path):
    print("\n🔄 Resuming training...")
    model = YOLO(weights_path)
else:
    print("\n🆕 Training from yolov8n.pt...")
    model = YOLO("yolov8n.pt")

model.train(data=yaml_path, epochs=10, imgsz=640)

# === Run Inference ===
print("\n🎥 Running real-time detection...")
model = YOLO("runs/detect/train/weights/best.pt")
model.predict(source=0, show=True, conf=0.5, stream=True)
