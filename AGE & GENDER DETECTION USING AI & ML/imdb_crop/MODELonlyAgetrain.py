import os
import numpy as np
import pandas as pd
import scipy.io
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

# Load metadata
mat_path = r"D:\1\2\PROJECT\AGE.GENDER\imdb_crop\imdb.mat"
meta_raw = scipy.io.loadmat(mat_path)
meta = meta_raw['imdb'][0][0]

full_path = meta['full_path'][0]
dob = meta['dob'][0]
photo_taken = meta['photo_taken'][0]

birth_year = np.floor(dob / 365.25 + 1970)
age = photo_taken - birth_year

df = pd.DataFrame({
    'path': [str(x[0]) for x in full_path],
    'age': age
})

# Filter ages between 0 and 100
df = df[(df['age'] > 0) & (df['age'] < 100)]
df = df.reset_index(drop=True)

print(f"Total images after filtering: {len(df)}")

# Optional sample for faster training
sample_size = 20000
if len(df) > sample_size:
    df = df.sample(sample_size, random_state=42).reset_index(drop=True)

# Load images and age labels
def load_image(img_path, target_size=(128, 128)):
    base_folder = r"D:\1\2\PROJECT\AGE.GENDER\imdb_crop"
    full_img_path = os.path.join(base_folder, img_path)
    if not os.path.exists(full_img_path):
        print(f"Image not found: {full_img_path}")
        return None
    try:
        img = cv2.imread(full_img_path)
        img = cv2.resize(img, target_size)
        img = img / 255.0
        return img
    except Exception as e:
        print(f"Error loading image {full_img_path}: {e}")
        return None

X, y_age = [], []

for _, row in df.iterrows():
    img = load_image(row['path'])
    if img is not None:
        X.append(img)
        y_age.append(row['age'])

print(f"Images loaded: {len(X)}")

X = np.array(X)
y_age = np.array(y_age, dtype=np.float32)

if len(X) == 0:
    raise RuntimeError("No images loaded. Check paths.")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_age, test_size=0.2, random_state=42)

# CNN model
input_layer = Input(shape=(128, 128, 3))
x = Conv2D(32, (3,3), activation='relu')(input_layer)
x = BatchNormalization()(x)
x = MaxPooling2D((2,2))(x)

x = Conv2D(64, (3,3), activation='relu')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2,2))(x)

x = Conv2D(128, (3,3), activation='relu')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2,2))(x)

x = Flatten()(x)
x = Dropout(0.5)(x)

age_output = Dense(1, activation='linear')(x)  # Regression output

model = Model(inputs=input_layer, outputs=age_output)
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

model.summary()

# Train
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

# Evaluate
loss, mae = model.evaluate(X_test, y_test)
print(f"Test MAE: {mae:.2f} years")

# Save model
model.save("age_model.h5")
print("Saved model as 'age_model.h5'")
