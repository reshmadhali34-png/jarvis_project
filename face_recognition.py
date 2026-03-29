import cv2
import os

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/model.yml")

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# 🔥 AUTO LOAD NAMES (MATCHES TRAINING)
names = sorted(os.listdir("dataset"))

print("Loaded Names:", names)

cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    if not ret:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        print("ID:", id, "Confidence:", confidence)

        if confidence < 70 and id < len(names):
            name = names[id]
        else:
            name = "Unknown"

        cv2.putText(img, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Recognition', img)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()