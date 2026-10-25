"""Batch age + gender prediction over the images in ``samples/``.

Uses the two separate single-task models (``models/gender_model.h5`` and
``models/age_model.h5``) instead of the joint model.

Run:  python predict_on_images.py      (press any key to advance, 'q' to quit)
"""

import json
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
SAMPLES_DIR = BASE_DIR / "samples"

IMG_SIZE = 128
MAX_AGE = 80  # the age head was trained on ages normalised to this range
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def load_gender_labels() -> list[str]:
    """Read the class order saved at training time (falls back to alphabetical)."""
    indices_path = MODELS_DIR / "gender_class_indices.json"
    if indices_path.exists():
        indices = json.loads(indices_path.read_text(encoding="utf-8"))
        if indices:
            return [name for name, _ in sorted(indices.items(), key=lambda kv: kv[1])]
    return ["men", "women"]


def preprocess(image_bgr: np.ndarray) -> np.ndarray:
    img = cv2.resize(image_bgr, (IMG_SIZE, IMG_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)


def predict_gender(model, input_img: np.ndarray, labels: list[str]) -> str:
    prob = float(model.predict(input_img, verbose=0)[0][0])
    return labels[int(prob > 0.5)]


def predict_age(model, input_img: np.ndarray) -> float:
    preds = model.predict(input_img, verbose=0)
    if preds.shape[1] == 1:
        age = float(preds[0][0])
        if 0 <= age <= 1:
            age *= MAX_AGE
    else:
        # Soft-classification head: expected value over the age bins.
        age_prob = preds[0]
        if not np.isclose(np.sum(age_prob), 1.0, atol=1e-3):
            age_prob = tf.nn.softmax(age_prob).numpy()
        age = float(np.sum(np.arange(len(age_prob)) * age_prob))
    return max(0.0, age)


def main() -> None:
    labels = load_gender_labels()

    try:
        gender_model = load_model(MODELS_DIR / "gender_model.h5")
        print("Gender model loaded.")
    except Exception as exc:  # noqa: BLE001 - report and continue with age only
        gender_model = None
        print(f"Could not load gender model: {exc}")

    try:
        age_model = load_model(MODELS_DIR / "age_model.h5")
        print("Age model loaded.")
    except Exception as exc:  # noqa: BLE001 - report and continue with gender only
        age_model = None
        print(f"Could not load age model: {exc}")

    image_files = sorted(
        p for p in SAMPLES_DIR.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not image_files:
        raise SystemExit(f"No images found in {SAMPLES_DIR}")

    for image_path in image_files:
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"Could not read {image_path.name}")
            continue

        input_img = preprocess(image)
        gender = predict_gender(gender_model, input_img, labels) if gender_model else "N/A"
        age = f"{predict_age(age_model, input_img):.1f} years" if age_model else "N/A"

        cv2.putText(
            image, f"Gender: {gender}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
        cv2.putText(
            image, f"Age: {age}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )

        print(f"{image_path.name}: gender={gender}, age={age}")
        cv2.imshow(f"Prediction - {image_path.name}", image)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
