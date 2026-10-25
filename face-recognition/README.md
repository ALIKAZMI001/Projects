# Face Recognition

Two complete face-recognition implementations behind the same webcam demo, plus a
Tkinter desktop app that drives them. Comparing them shows the trade-off clearly:
the CNN generalises, the KNN baseline is instant to train.

| | `cnn/` | `knn/` |
| --- | --- | --- |
| Model | Keras CNN (224×224, 2 classes + unknown fallback) | KNN, k=5, on raw 50×50 pixels |
| Training | Transfer-style training on collected images | Fits in-memory at startup |
| Input | Face crop → 224×224 → `/255` | Face crop → 50×50 → flatten (7 500 features) |
| Strength | Handles lighting/pose variation | No training step, trivial to extend |
| Weakness | Needs many images per person | Sensitive to alignment and lighting |

## Layout

```
face-recognition/
├── cnn/
│   ├── collect_faces.py          # capture images/<name>/*.jpg  (500 per person)
│   ├── recognize.py              # live webcam classification
│   ├── keras_model.h5            # trained classifier
│   ├── haarcascade_frontalface_default.xml
│   └── images/<name>/            # training images
└── knn/
    ├── add_faces.py              # capture + append to the pickled dataset
    ├── recognize.py              # live webcam KNN recognition
    ├── app.py                    # Tkinter login + launcher UI
    ├── s.png                     # app background
    └── data/
        ├── faces_data.pkl        # flattened face vectors
        ├── names.pkl             # matching labels
        └── haarcascade_frontalface_default.xml
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

CNN pipeline:

```bash
cd cnn
python collect_faces.py         # build a dataset for a new person
python recognize.py             # press 'q' to quit
```

KNN pipeline:

```bash
cd knn
python add_faces.py alice       # 100 faces → data/*.pkl
python recognize.py
```

Desktop app:

```bash
cd knn
python app.py
```

## App configuration

The Tkinter app reads its demo credentials from the environment — nothing is
hardcoded:

```bash
set FACE_APP_USERS=ali,junaidahmed          # comma-separated usernames
set FACE_APP_PASSWORD=demo
python app.py
```

This is a classroom demo UI, **not** an authentication system.

## Implementation notes

- Face detection uses OpenCV's Haar cascade in both pipelines; recognition only runs
  on the cropped face, which keeps the feature space consistent.
- `add_faces.py` appends to the existing pickle files, so people can be enrolled
  incrementally without retraining anything.
- The app launches the capture/recognition scripts in worker threads with
  `sys.executable` and the correct working directory, so the UI never freezes and
  the scripts find their relative data paths.
- `keras_model.h5` was produced in a Teachable-Machine-style workflow; edit
  `CLASS_NAMES` in `cnn/recognize.py` if you retrain with a different label set.

## Stack

`tensorflow` · `opencv-python` · `scikit-learn` · `numpy` · `pillow` · `tkinter`
