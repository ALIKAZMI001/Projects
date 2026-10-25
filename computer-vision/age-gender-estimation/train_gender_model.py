"""Train a binary gender classifier on the pre-cropped ``data/gender`` folders.

Expects ``data/gender/men/`` and ``data/gender/women/``.

Run:  python train_gender_model.py
"""

import json
from pathlib import Path

from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "gender"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 10


def main() -> None:
    datagen = ImageDataGenerator(rescale=1.0 / 255, validation_split=0.2)

    train_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        subset="training",
        shuffle=True,
    )
    val_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        subset="validation",
        shuffle=False,
    )

    print("Class indices:", train_generator.class_indices)
    # Persist the label mapping so inference always matches training order.
    (MODELS_DIR / "gender_class_indices.json").write_text(
        json.dumps(train_generator.class_indices, indent=2), encoding="utf-8"
    )

    model = Sequential(
        [
            Conv2D(32, (3, 3), activation="relu", input_shape=(128, 128, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation="relu"),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation="relu"),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dropout(0.5),
            Dense(64, activation="relu"),
            Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.summary()

    model.fit(train_generator, validation_data=val_generator, epochs=EPOCHS)

    out_path = MODELS_DIR / "gender_model.h5"
    model.save(out_path)
    print(f"Saved model to {out_path}")


if __name__ == "__main__":
    main()
