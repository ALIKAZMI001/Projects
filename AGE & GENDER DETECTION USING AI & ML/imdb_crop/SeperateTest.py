import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.nn import softmax
import tensorflow as tf
import os

# --- Load models ---
gender_model_path = r'D:\1\2\PROJECT\AGE.GENDER\imdb_crop\gender_model.h5'
age_model_path = r'D:\1\2\PROJECT\AGE.GENDER\imdb_crop\age_model.h5'

try:
    gender_model = load_model(gender_model_path)
    print("✅ Gender model loaded.")
except Exception as e:
    gender_model = None
    print(f"❌ Error loading gender model: {e}")

try:
    age_model = load_model(age_model_path)
    print("✅ Age model loaded.")
except Exception as e:
    age_model = None
    print(f"❌ Error loading age model: {e}")

# --- Constants ---
IMG_SIZE = 128
gender_labels = ['men', 'women']
MAX_AGE = 80  # Adjust based on training

def preprocess(image):
    """Resize and normalize image."""
    img = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255.0
    return np.expand_dims(img, axis=0)

# --- Path to image or folder ---
image_folder = r'D:\1\2\PROJECT\AGE.GENDER\test_images'  # Change this to your folder
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Failed to load image: {image_path}")
        continue

    input_img = preprocess(image)

    # --- Gender prediction ---
    gender_text = "N/A"
    if gender_model:
        gender_prob = gender_model.predict(input_img, verbose=0)[0][0]
        gender_text = gender_labels[int(gender_prob > 0.5)]

    # --- Age prediction ---
    age_text = "N/A"
    if age_model:
        try:
            preds = age_model.predict(input_img, verbose=0)
            if preds.shape[1] == 1:
                age_pred = preds[0][0]
                if 0 <= age_pred <= 1:
                    age_pred = age_pred * MAX_AGE
            else:
                ages = np.arange(preds.shape[1])
                age_prob = preds[0]
                if not np.isclose(np.sum(age_prob), 1.0, atol=1e-3):
                    age_prob = tf.nn.softmax(age_prob).numpy()
                age_pred = np.sum(ages * age_prob)

            age_pred = max(0, age_pred)
            age_text = f"{age_pred:.1f} years"
        except Exception as e:
            print(f"❌ Age prediction failed for {image_file}: {e}")

    # --- Show result ---
    output_img = image.copy()
    cv2.putText(output_img, f"Gender: {gender_text}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(output_img, f"Age: {age_text}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow(f'Prediction - {image_file}', output_img)
    print(f"🖼️ Processed {image_file} | Gender: {gender_text}, Age: {age_text}")
    cv2.waitKey(0)  # Press any key to continue to next image

cv2.destroyAllWindows()
