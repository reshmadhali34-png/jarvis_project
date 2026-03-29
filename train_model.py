import cv2
import numpy as np
import os

dataset_path = "dataset"

# Create recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_dict = {}
current_label = 0

# 🔥 SORT folders to keep order fixed
users = sorted(os.listdir(dataset_path))

for user in users:
    user_path = os.path.join(dataset_path, user)

    # Skip if not a folder
    if not os.path.isdir(user_path):
        continue

    print(f"Processing {user}...")

    label_dict[current_label] = user

    for img_name in os.listdir(user_path):
        img_path = os.path.join(user_path, img_name)

        # Read image in grayscale
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # Skip if image not loaded
        if img is None:
            continue

        faces.append(img)
        labels.append(current_label)

    current_label += 1

# ❗ Check if data exists
if len(faces) == 0:
    print("❌ No images found. Please capture faces first.")
    exit()

# Train model
recognizer.train(faces, np.array(labels))

# Save model
os.makedirs("trainer", exist_ok=True)
recognizer.save("trainer/model.yml")

print("\n✅ Training Complete!")
print("📌 Label Mapping:")
for key, value in label_dict.items():
    print(f"{key} → {value}")