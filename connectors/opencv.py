from tkinter import *
import cv2
from PIL import Image
import threading
from os import path
import pickle
import time
import datetime
from datetime import date
from skimage.metrics import structural_similarity as ssim
import os

basepath = path.dirname(__file__)
filepath_labels = path.abspath(path.join(basepath, "..", "files", "labels.pickle"))
filepath_trainner_frontalface = path.abspath(path.join(basepath, "..", "files", "trainner.yml"))
photosPath = path.abspath(path.join(basepath, "..", "files", "UknowFaces"))

def opencv_import(cap, face_cascade_frontalface, stop_thread, cap2):
    def faceDetection(test_img):
            gray_img=cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
            faces_frontalface=face_cascade_frontalface.detectMultiScale(gray_img,scaleFactor=1.1,minNeighbors=5)
            return faces_frontalface,gray_img

    def faceDetection2(test_img2):
            gray_img2=cv2.cvtColor(test_img2,cv2.COLOR_BGR2GRAY)
            faces_frontalface2=face_cascade_frontalface.detectMultiScale(gray_img2,scaleFactor=1.1,minNeighbors=5)
            return faces_frontalface2,gray_img2

    def call_to_db_insert(predict_name):
            from connector import Insert_to_db
            Insert_to_db(predict_name)

    def call_to_db_insert2(predict_name2):
            from connector import Insert_to_db2
            Insert_to_db2(predict_name2)

    global last_saved_time, last_saved_time2
    time_interval = 3 
    last_saved_time = time.time() - time_interval

    time_interval2 = 3 
    last_saved_time2 = time.time() - time_interval2 

    lables = {}
    labels2 = {}
    with open(filepath_labels, "rb") as f:
            og_labels = pickle.load(f)
            lables = {v:k for k, v in og_labels.items()}
            lables2 = {v:k for k, v in og_labels.items()}

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(photosPath, today)
    folder_path2 = os.path.join(photosPath, today)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.exists(folder_path2):
        os.makedirs(folder_path2)
        
    global current_person, current_person2
    current_person = 0
    current_person2 = 0
    person_images = {}
    person_images2 = {}

    stop_thread.clear()
    global face_recognizer_frontalface
    face_recognizer_frontalface=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer_frontalface.read(filepath_trainner_frontalface)

    thread = None
    global pTime
    pTime=0

    def update_frame():
        ret, test_img = cap.read()
        ret2, test_img2 = cap2.read()                                                           #CAMERA 2

        if ret:
                faces_detected_frontalface, gray_img = faceDetection(test_img)

                global_faces_detected_frontalface = faces_detected_frontalface

                for face in faces_detected_frontalface:
                        (x, y, w, h) = face
                        rol_gray = gray_img[y:y+h, x:x+h]
                        label, confidence = face_recognizer_frontalface.predict(rol_gray)
                        predict_name = lables[label]

                        if confidence < 85:

                                current_time = time.time()
                                global last_saved_time
                                if current_time - last_saved_time >= time_interval:
                                        call_to_db_insert(predict_name)
                                        last_saved_time = current_time

                        else:
                                if len(faces_detected_frontalface) > 0:
                                        for (x, y, w, h) in faces_detected_frontalface:
                                                face = test_img[y:y+h, x:x+w]
                                                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                                                face = cv2.resize(face, (256, 256))
                                                max_similarity = 0
                                                similar_folder = None
                                                similar_folder2 = None

                                                for folder, images in person_images.items():
                                                        for filename, image in images.items():
                                                                similarity = ssim(image, face)
                                                                if similarity > max_similarity:
                                                                        max_similarity = similarity
                                                                        similar_folder = folder

                                                if max_similarity > 0.7:
                                                        timestamp = datetime.datetime.now().strftime("%H-%M-%S")
                                                        filename = os.path.join(similar_folder, f'{timestamp}.jpg')
                                                        cv2.imwrite(filename, face)
                                                        person_images[similar_folder][f'{timestamp}.jpg'] = face   

                                                else:
                                                        global current_person
                                                        current_person += 1
                                                        current_person_folder = os.path.join(folder_path, f'person_{current_person}')
                                                        os.makedirs(current_person_folder, exist_ok=True)
                                                        timestamp = datetime.datetime.now().strftime("%H-%M-%S")
                                                        filename = os.path.join(current_person_folder, f'{timestamp}.jpg')
                                                        cv2.imwrite(filename, face)
                                                        person_images[current_person_folder] = {f'{timestamp}.jpg': face}
                
        if ret2:
                faces_detected_frontalface2, gray_img2 = faceDetection2(test_img2)
                global_faces_detected_frontalface2 = faces_detected_frontalface2

                for face in faces_detected_frontalface2:
                        (x, y, w, h) = face
                        rol_gray2 = gray_img2[y:y+h, x:x+h]
                        label2, confidence2 = face_recognizer_frontalface.predict(rol_gray2)
                        predict_name2 = lables2[label2]

                        if confidence2 < 85:

                                current_time2 = time.time()
                                global last_saved_time2
                                if current_time2 - last_saved_time2 >= time_interval2:
                                        call_to_db_insert2(predict_name2)
                                        last_saved_time2 = current_time2

                        else:
                                if len(faces_detected_frontalface2) > 0:
                                        for (x, y, w, h) in faces_detected_frontalface2:
                                                face2 = test_img2[y:y+h, x:x+w]
                                                face2 = cv2.cvtColor(face2, cv2.COLOR_BGR2GRAY)
                                                face2 = cv2.resize(face2, (256, 256))
                                                max_similarity2 = 0
                                                similar_folder2 = None

                                                for folder2, images2 in person_images2.items():
                                                        for filename2, image2 in images2.items():
                                                                similarity2 = ssim(image2, face2)
                                                                if similarity2 > max_similarity2:
                                                                        max_similarity2 = similarity2
                                                                        similar_folder2 = folder2

                                                if max_similarity2 > 0.7:
                                                        timestamp2 = datetime.datetime.now().strftime("%H-%M-%S")
                                                        filename2 = os.path.join(similar_folder2, f'{timestamp2}.jpg')
                                                        cv2.imwrite(filename2, face2)
                                                        person_images2[similar_folder2][f'{timestamp2}.jpg'] = face2                         

                                                else:
                                                        global current_person2
                                                        current_person2 += 1
                                                        current_person_folder2 = os.path.join(folder_path2, f'person_{current_person2}')
                                                        os.makedirs(current_person_folder2, exist_ok=True)
                                                        timestamp2 = datetime.datetime.now().strftime("%H-%M-%S")
                                                        filename2 = os.path.join(current_person_folder2, f'{timestamp2}.jpg')
                                                        cv2.imwrite(filename2, face2)
                                                        person_images2[current_person_folder2] = {f'{timestamp2}.jpg': face2}        

        from RGBCamera import opencv_RGBCamera
        opencv_RGBCamera(global_faces_detected_frontalface, gray_img, test_img, face_recognizer_frontalface, global_faces_detected_frontalface2, gray_img2, test_img2)

        from GrayCamera import opencv_GrayCamera
        opencv_GrayCamera(global_faces_detected_frontalface, gray_img, test_img, face_recognizer_frontalface, global_faces_detected_frontalface2, gray_img2, test_img2)

        from RGBCameraNoRectanglesLabels import opencv_RGBCameraNoRectanglesLabels
        opencv_RGBCameraNoRectanglesLabels(test_img, test_img2)

        from GrayCameraNoRectanglesLabels import opencv_GrayCameraNoRectanglesLabels
        opencv_GrayCameraNoRectanglesLabels(gray_img, gray_img2)


        # if not stop_thread.is_set():
        #         update_frame()
        #         time.sleep(0)
    
    def run_update_frame():
        while not stop_thread.is_set():
               update_frame()
               time.sleep(0)

    #stop_thread = threading.Event()

    thread = threading.Thread(target=run_update_frame)
    thread.start()