from os import path
import numpy as np
from PIL import Image
import cv2
import pickle
import os

basepath = path.dirname(__file__)
photosPath = path.abspath(path.join(basepath, "..", "files", "faces"))
haarcascades_frontalface_path = path.abspath(path.join(basepath, "..", "files", "haarcascades","haarcascade_frontalface_default.xml"))

def trainner_start():

    face_cascade_frontalface = cv2.CascadeClassifier(haarcascades_frontalface_path)

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids ={}
    y_labels = []
    x_train = []

    for root, dirs, files in os.walk(photosPath):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
                if label in label_ids:
                    pass
                else:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]
                pil_image = Image.open(path).convert("L")
                
                size = (550, 550)
                final_image = pil_image.resize(size, Image.ANTIALIAS)
                image_array = np.array(final_image, "uint8")

                faces_frontalface = face_cascade_frontalface.detectMultiScale(image_array, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in faces_frontalface:
                    roi = image_array[y:y+h, x:x+w]
                    print(id_)
                    print(roi)
                    x_train.append(roi)
                    y_labels.append(id_)

    if not os.path.exists("files"):
        os.makedirs("files")

    with open("files/labels.pickle", "wb") as f:
        pickle.dump(label_ids, f)


    picklel = pickle.load(open("files/labels.pickle", "rb"))
    print(picklel)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("files/trainner.yml")

    from connector import insert_osobe_to_db
    insert_osobe_to_db()