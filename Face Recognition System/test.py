from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
import threading
from datetime import datetime
from pathlib import Path
from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)


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

names_file = data_dir / 'names.pkl'
with open(names_file, 'rb') as f:
    LABELS = pickle.load(f)

faces_data_file = data_dir / 'faces_data.pkl'
with open(faces_data_file, 'rb') as f:
    FACES = pickle.load(f)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES,LABELS)

imgBackground=cv2.imread("background.png")

COL_NAMES=['NAME','TIME']
def listen_for_exit():
    while True:
        command = input()
        if command.lower() == "exit":
            print("Exiting program...")
            os._exit(0)  


exit_thread = threading.Thread(target=listen_for_exit)
exit_thread.daemon = True  
exit_thread.start()

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1,-1) 
        output=knn.predict(resized_img)
        ts=time.time()
        date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist=os.path.isfile("attendance/attendance_"+date+".csv")
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(0,0,255),-1)
        cv2.putText(frame,str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
        attendance=[str(output[0]),str(timestamp)]
    imgBackground[162:162 + 480, 55:55 +640]=frame
    cv2.imshow("Frame", imgBackground)
    if cv2.waitKey(1) & 0xFF ==ord('o'):
        speak("Attendance taken")
        time.sleep(3)
        if exist:
            with open("attendance/attendance_"+date+".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("attendance/attendance_"+date+".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
    
    
video.release()
cv2.destroyAllWindows()




