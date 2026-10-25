# Age & Gender Estimation

Multi-task CNN that predicts **gender (2 classes)** and **age (regression)** from a
single face crop. Trained on the [IMDB-WIKI](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/)
face dataset.

<!-- Add a screenshot / GIF of predict_webcam.py here — see README notes at repo root. -->

## What's implemented

- **Joint model** — one shared convolutional trunk with two heads
  (`gender_output`: softmax over 2 classes, `age_output`: linear regression),
  trained with a weighted sum of categorical cross-entropy and MSE.
- **Two single-task variants** — a standalone age regressor (with batch
  normalisation) and a standalone gender classifier trained straight from
  `data/gender/{men,women}` folders.
- **Live inference** — Haar-cascade face detection, per-face prediction, labelled
  bounding boxes.
- **Batch inference** — runs the two single-task models over `samples/`.

## Layout

```
age-gender-estimation/
├── train_joint_model.py      # two-head CNN  → models/age_gender_model.h5
├── train_age_model.py        # age-only CNN  → models/age_model.h5
├── train_gender_model.py     # gender-only   → models/gender_model.h5
├── predict_webcam.py         # live webcam demo (joint model)
├── predict_on_images.py      # batch demo (separate models)
├── models/                   # trained weights + gender class mapping
├── data/
│   ├── imdb.mat              # IMDB-WIKI metadata (paths, gender, dob, photo year)
│   └── gender/{men,women}/   # pre-cropped faces for the gender classifier
└── samples/                  # test faces
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python predict_webcam.py        # live demo, press 'q' to quit
python predict_on_images.py     # batch demo over samples/
```

Retrain (20 000-image sample, 10 epochs by default — edit the constants at the top
of each script to change it):

```bash
python train_joint_model.py
python train_age_model.py
python train_gender_model.py
```

## Implementation notes

- Images are resized to **128×128**, converted BGR→RGB and scaled to `[0, 1]` —
  the exact same preprocessing is applied at train and inference time.
- `train_gender_model.py` writes `models/gender_class_indices.json` so inference
  never has to guess the class order (alphabetical from `flow_from_directory`:
  `men → 0`, `women → 1`).
- Age is a regression target in years; the joint model predicts it directly, while
  the age-only model uses batch normalisation between conv blocks to stabilise
  training.
- All paths are resolved relative to the script (`Path(__file__).parent`), so the
  project runs from any working directory.

## Stack

`tensorflow` · `opencv-python` · `scikit-learn` · `pandas` · `scipy` · `numpy`
