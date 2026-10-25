"""Train an age-regression CNN on the IMDB-WIKI face crops.

Run:  python train_age_model.py
"""

from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import scipy.io
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import (
    BatchNormalization,
    Conv2D,
    Dense,
    Dropout,
    Flatten,
    Input,
    MaxPooling2D,
)
from tensorflow.keras.models import Model

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

IMG_SIZE = 128
SAMPLE_SIZE = 20_000
EPOCHS = 10
BATCH_SIZE = 32


def load_metadata() -> pd.DataFrame:
    meta = scipy.io.loadmat(DATA_DIR / "imdb.mat")["imdb"][0][0]

    full_path = meta["full_path"][0]
    dob = meta["dob"][0]
    photo_taken = meta["photo_taken"][0]

    birth_year = np.floor(dob / 365.25 + 1970)
    age = photo_taken - birth_year

    df = pd.DataFrame({"path": [str(p[0]) for p in full_path], "age": age})
    df = df[(df["age"] > 0) & (df["age"] < 100)].reset_index(drop=True)
    print(f"Rows available after filtering: {len(df)}")

    if len(df) > SAMPLE_SIZE:
        df = df.sample(SAMPLE_SIZE, random_state=42).reset_index(drop=True)
    return df


def load_image(relative_path: str):
    img_path = DATA_DIR / relative_path
    if not img_path.exists():
        return None
    img = cv2.imread(str(img_path))
    if img is None:
        return None
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    return img / 255.0


def build_model() -> Model:
    inputs = Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = Conv2D(32, (3, 3), activation="relu")(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)

    x = Conv2D(64, (3, 3), activation="relu")(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)

    x = Conv2D(128, (3, 3), activation="relu")(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)

    x = Flatten()(x)
    x = Dropout(0.5)(x)
    outputs = Dense(1, activation="linear", name="age_output")(x)

    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model


def main() -> None:
    df = load_metadata()

    images, ages = [], []
    for row in df.itertuples():
        img = load_image(row.path)
        if img is not None:
            images.append(img)
            ages.append(row.age)

    print(f"Images loaded: {len(images)}")
    if not images:
        raise RuntimeError("No images loaded — check data/imdb.mat and the image paths.")

    X = np.asarray(images)
    y = np.asarray(ages, dtype=np.float32)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = build_model()
    model.summary()

    model.fit(
        X_train,
        y_train,
        validation_data=(X_test, y_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
    )

    loss, mae = model.evaluate(X_test, y_test)
    print(f"Test MAE: {mae:.2f} years")

    out_path = MODELS_DIR / "age_model.h5"
    model.save(out_path)
    print(f"Saved model to {out_path}")


if __name__ == "__main__":
    main()
