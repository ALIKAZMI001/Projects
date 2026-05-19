import os
import numpy as np
import pandas as pd
import scipy.io
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import tensorflow as tf

# ========== STEP 1: Load .mat file ==========
meta = scipy.io.loadmat('imdb.mat')
full_path = meta['imdb']['full_path'][0][0].flatten()
gender = meta['imdb']['gender'][0][0].flatten()
dob = meta['imdb']['dob'][0][0].flatten()
photo_taken = meta['imdb']['photo_taken'][0][0].flatten()

birth_year = np.floor(dob / 365.25 + 1970)
age = photo_taken - birth_year

df = pd.DataFrame({
    'path': [str(x[0]) for x in full_path],
    'gender': gender,
    'age': age
})

# Clean data
df = df[(df['gender'] == 0) | (df['gender'] == 1)]
df = df[(df['age'] > 0) & (df['age'] < 100)]

print(f"Total rows available after cleaning: {len(df)}")

# Optional: sample subset or keep all if less than 20000
sample_size = 20000
if len(df) > sample_size:
    df = df.sample(sample_size, random_state=42).reset_index(drop=True)
else:
    df = df.reset_index(drop=True)

# ========== STEP 2: Load images and labels ==========
def load_image(img_path, target_size=(128, 128)):
    base_folder =  r"D:\1\2\PROJECT\AGE.GENDER\imdb_crop"
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

X, y_gender, y_age = [], [], []

for _, row in df.iterrows():
    img = load_image(row['path'])
    if img is not None:
        X.append(img)
        y_gender.append(int(row['gender']))
        y_age.append(row['age'])

print(f"Images loaded: {len(X)}")

X = np.array(X)
y_gender = to_categorical(y_gender, num_classes=2)
y_age = np.array(y_age)

if len(X) == 0:
    raise RuntimeError("No images were loaded. Check the image paths and base folder.")

# ========== STEP 3: Train-test split ==========
X_train, X_test, y_gender_train, y_gender_test, y_age_train, y_age_test = train_test_split(
    X, y_gender, y_age, test_size=0.2, random_state=42)

# ========== STEP 4: Build the CNN model ==========
input_layer = Input(shape=(128, 128, 3))
x = Conv2D(32, (3,3), activation='relu')(input_layer)
x = MaxPooling2D((2,2))(x)
x = Conv2D(64, (3,3), activation='relu')(x)
x = MaxPooling2D((2,2))(x)
x = Conv2D(128, (3,3), activation='relu')(x)
x = MaxPooling2D((2,2))(x)
x = Flatten()(x)
x = Dropout(0.5)(x)

gender_output = Dense(2, activation='softmax', name='gender_output')(x)
age_output = Dense(1, activation='linear', name='age_output')(x)

model = Model(inputs=input_layer, outputs=[gender_output, age_output])
model.compile(optimizer='adam',
              loss={'gender_output': 'categorical_crossentropy', 'age_output': 'mse'},
              metrics={'gender_output': 'accuracy', 'age_output': 'mae'})

model.summary()

# ========== STEP 5: Train ==========
model.fit(X_train, {'gender_output': y_gender_train, 'age_output': y_age_train},
          validation_data=(X_test, {'gender_output': y_gender_test, 'age_output': y_age_test}),
          epochs=10, batch_size=32)

# ========== STEP 6: Evaluate ==========
loss, gender_loss, age_loss, gender_acc, age_mae = model.evaluate(
    X_test, {'gender_output': y_gender_test, 'age_output': y_age_test})

print(f"Gender Accuracy: {gender_acc:.2f}")
print(f"Age MAE: {age_mae:.2f} years")


# ========== STEP 7: Save model ==========
model.save("age_gender_model.h5")
print("Model saved as 'age_gender_model.h5'")