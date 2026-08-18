import cv2
import numpy as np
import os
import pickle
import sys

# Function to handle user input if not provided via command line
def get_name():
    if len(sys.argv) > 1:
        return sys.argv[1].strip().lower()
    else:
        return input("Enter Your Name: ").strip().lower()

# Initialize webcam and Haar Cascade Classifier
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Get name from command line argument or user input
nameID = get_name()
path = os.path.join('images', nameID)

# Ensure the directory exists
if not os.path.exists(path):
    os.makedirs(path)
else:
    print("Name Already Taken. Please use a different name.")
    sys.exit(1)  # Exit if the name already exists

# List to store face data
faces_data = []
count = 0

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # Save raw face images
        count += 1
        face_img = frame[y:y+h, x:x+w]
        image_path = os.path.join(path, f'{count}.jpg')
        print(f"Creating Images.........{image_path}")
        cv2.imwrite(image_path, face_img)
        
        # Resize face image for data storage
        resized_img = cv2.resize(face_img, (50, 50))
        faces_data.append(resized_img)
        
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    # Display the frame
    cv2.imshow("WindowFrame", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Exit on ESC key
        break
    
    # Stop if 100 images are collected
    if count >= 100:
        break

video.release()
cv2.destroyAllWindows()

# Convert faces_data list to numpy array
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)

# Directory for pickle files
data_dir = 'data/'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Save names to pickle file
names_file = os.path.join(data_dir, 'names.pkl')
if os.path.exists(names_file):
    with open(names_file, 'rb') as f:
        names = pickle.load(f)
    names += [nameID] * 100
else:
    names = [nameID] * 100
with open(names_file, 'wb') as f:
    pickle.dump(names, f)

# Save face data to pickle file
faces_data_file = os.path.join(data_dir, 'faces_data.pkl')
if os.path.exists(faces_data_file):
    with open(faces_data_file, 'rb') as f:
        existing_faces = pickle.load(f)
    faces_data = np.append(existing_faces, faces_data, axis=0)
with open(faces_data_file, 'wb') as f:
    pickle.dump(faces_data, f)
