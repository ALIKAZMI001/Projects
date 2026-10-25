# YOLOv8 Face Detection

A custom **YOLOv8n** detector fine-tuned on face crops captured from my own webcam.
The whole pipeline — data collection, labelling, splitting, training, live
inference — lives in this folder.

## Pipeline

```
webcam ──► MediaPipe face detection ──► cropped face + YOLO label
                                              │
                                  75/25 train-val split
                                              │
                              fine-tune yolov8n.pt (10 epochs)
                                              │
                              runs/detect/train/weights/best.pt
                                              │
                                   live webcam inference
```

## Layout

```
yolo-face-detection/
├── train.py              # capture → split → write data.yaml → train
├── predict.py            # real-time webcam detection
├── data.yaml             # dataset config (class names)
├── dataset/
│   ├── images/{train,val}/
│   └── labels/{train,val}/
├── runs/detect/train/    # training artifacts: weights, curves, confusion matrix
└── yolov8n.pt            # base COCO checkpoint used for fine-tuning
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python predict.py               # uses runs/detect/train/weights/best.pt
```

Retrain on a new person:

```bash
python train.py
```

`train.py` asks for a name, captures 200 face crops, writes a full-frame YOLO label
for each crop, moves 25% into validation, regenerates `data.yaml`, then resumes from
`last.pt` if a checkpoint exists or starts from `yolov8n.pt` otherwise.

## Training results

`runs/detect/train/` contains the full run: `results.png`, `results.csv`,
`PR_curve.png`, `F1_curve.png`, `confusion_matrix.png`, and the `best.pt` /
`last.pt` weights.

> **Note on the dataset:** the `images/` folders are empty in this repo — the face
> crops are personal photos and were intentionally not committed. `train.py`
> regenerates them from a webcam in a couple of minutes. The label files and
> `data.yaml` from the original run are kept for reference.

## Stack

`ultralytics` · `mediapipe` · `opencv-python`
