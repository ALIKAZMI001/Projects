"""Train a single CNN with two heads: gender classification + age regression.

Dataset: IMDB-WIKI face crops (``data/imdb.mat`` metadata + ``data/imdb_crop/``
images, or ``data/gender/{men,women}`` for the pre-cropped subset).

Run:  python train_joint_model.py
"""

from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import scipy.io
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, Input, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

IMG_SIZE = 128
SAMPLE_SIZE = 20_000
EPOCHS = 10
BATCH_SIZE = 32


def load_metadata() -> pd.DataFrame:
    """Parse the MATLAB metadata file into a (path, gender, age) table."""
    meta = scipy.io.loadmat(DATA_DIR / "imdb.mat")["imdb"][0][0]

    full_path = meta["full_path"][0]
    gender = meta["gender"][0]
    dob = meta["dob"][0]
    photo_taken = meta["photo_taken"][0]

    birth_year = np.floor(dob / 365.25 + 1970)
    age = photo_taken - birth_year

    df = pd.DataFrame(
        {
            "path": [str(p[0]) for p in full_path],
            "gender": gender,
            "age": age,
        }
    )

    # Keep only labelled genders and plausible ages.
    df = df[df["gender"].isin([0, 1])]
    df = df[(df["age"] > 0) & (df["age"] < 100)]
    print(f"Rows available after cleaning: {len(df)}")

    if len(df) > SAMPLE_SIZE:
        df = df.sample(SAMPLE_SIZE, random_state=42)
    return df.reset_index(drop=True)


def load_image(relative_path: str):
    """Read one face crop, resized and scaled to [0, 1]."""
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
    x = MaxPooling2D((2, 2))(x)
    x = Conv2D(64, (3, 3), activation="relu")(x)
    x = MaxPooling2D((2, 2))(x)
    x = Conv2D(128, (3, 3), activation="relu")(x)
    x = MaxPooling2D((2, 2))(x)
    x = Flatten()(x)
    x = Dropout(0.5)(x)

    gender_output = Dense(2, activation="softmax", name="gender_output")(x)
    age_output = Dense(1, activation="linear", name="age_output")(x)

    model = Model(inputs=inputs, outputs=[gender_output, age_output])
    model.compile(
        optimizer="adam",
        loss={"gender_output": "categorical_crossentropy", "age_output": "mse"},
        metrics={"gender_output": "accuracy", "age_output": "mae"},
    )
    return model


def main() -> None:
    df = load_metadata()

    images, genders, ages = [], [], []
    for row in df.itertuples():
        img = load_image(row.path)
        if img is not None:
            images.append(img)
            genders.append(int(row.gender))
            ages.append(row.age)

    print(f"Images loaded: {len(images)}")
    if not images:
        raise RuntimeError(
            "No images were loaded. Make sure data/imdb.mat and the image folder exist."
        )

    X = np.asarray(images)
    y_gender = to_categorical(genders, num_classes=2)
    y_age = np.asarray(ages)

    X_train, X_test, yg_train, yg_test, ya_train, ya_test = train_test_split(
        X, y_gender, y_age, test_size=0.2, random_state=42
    )

    model = build_model()
    model.summary()

    model.fit(
        X_train,
        {"gender_output": yg_train, "age_output": ya_train},
        validation_data=(X_test, {"gender_output": yg_test, "age_output": ya_test}),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
    )

    loss, gender_loss, age_loss, gender_acc, age_mae = model.evaluate(
        X_test, {"gender_output": yg_test, "age_output": ya_test}
    )
    print(f"Gender accuracy: {gender_acc:.2%}")
    print(f"Age MAE: {age_mae:.2f} years")

    out_path = MODELS_DIR / "age_gender_model.h5"
    model.save(out_path)
    print(f"Saved model to {out_path}")


if __name__ == "__main__":
    main()
