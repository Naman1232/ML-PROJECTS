import cv2
import pickle
import numpy as np
import os
from pathlib import Path


data_dir = Path('data')
data_dir.mkdir(parents=True, exist_ok=True)


video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not video.isOpened():
    print("DirectShow backend failed. Trying Video for Windows...")
    video = cv2.VideoCapture(0, cv2.CAP_VFW)

if not video.isOpened():
    print("Unable to open the camera. Please check the connection and try again.")
    exit()


cascade_path = r'C:\Users\Naman\Desktop\Face Recognition System\data\haarcascade_frontalface_default.xml'
facedetect = cv2.CascadeClassifier(cascade_path)

if facedetect.empty():
    print(f"Failed to load Haar Cascade from {cascade_path}. Check the path and file.")
    exit()

faces_data = []
i = 0


name = input("Enter your Name: ").strip()

if not name:
    print("Name cannot be empty.")
    exit()

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50))
        
        
        if len(faces_data) < 100 and i % 10 == 0:
            faces_data.append(resized_img)
        
        i += 1

        
        cv2.putText(frame, f"Count: {len(faces_data)}", (50, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

    cv2.imshow("Frame", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q') or len(faces_data) >= 100:
        break


video.release()
cv2.destroyAllWindows()


if len(faces_data) < 100:
    print(f"Only {len(faces_data)} faces were collected. Exiting.")
    exit()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)  


names_file = data_dir / 'names.pkl'

if not names_file.exists():
    names = [name] * 100
    with open(names_file, 'wb') as f:
        pickle.dump(names, f)
    print(f"Created '{names_file}' with {len(names)} names.")
else:
    with open(names_file, 'rb') as f:
        names = pickle.load(f)
    
    names += [name] * 100
    with open(names_file, 'wb') as f:
        pickle.dump(names, f)
    print(f"Appended {len([name]*100)} names to '{names_file}'.")


faces_data_file = data_dir / 'faces_data.pkl'

if not faces_data_file.exists():
    with open(faces_data_file, 'wb') as f:
        pickle.dump(faces_data, f)  
    print(f"Created '{faces_data_file}' with shape {faces_data.shape}.")
else:
    with open(faces_data_file, 'rb') as f:
        existing_faces = pickle.load(f)

    
    if isinstance(existing_faces, list):
        existing_faces = np.asarray(existing_faces)
    
    
    if existing_faces.ndim == 1:
       
        existing_faces = existing_faces.reshape(1, -1)

   
    if existing_faces.shape[1] == faces_data.shape[1]:
        updated_faces = np.append(existing_faces, faces_data, axis=0)
        with open(faces_data_file, 'wb') as f:
            pickle.dump(updated_faces, f)
        print(f"Appended faces data to '{faces_data_file}'. New shape: {updated_faces.shape}.")
    else:
        print("Shape mismatch. Cannot append faces data.")


