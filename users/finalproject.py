from PIL import Image

import numpy as np
from numpy import asarray
from numpy import expand_dims

import pickle
import cv2

def facereco(image_path,model,model_yolo):
    id_attendance=[]
    myfile = open(r"C:\Users\mreid\Desktop\projectweb\smartface\data4.pkl", "rb")
    database = pickle.load(myfile)
    myfile.close()
    img=cv2.imread(image_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = model_yolo.predict(source=img)
    gbr = Image.fromarray(img)
    gbr_array = asarray(gbr)
    faces=results[0].boxes.xyxy
    for x1,y1,x2,y2 in faces :
        x1=int(x1)
        y1=int(y1)
        x2=int(x2)
        y2=int(y2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        face=img[y1:y2,x1:x2]
        face = Image.fromarray(face)                       
        face = face.resize((160,160))
        face = asarray(face)
        face = expand_dims(face, axis=0)
        signature = model.embeddings(face)
        min_dist=100
        identity=' '
        
        for key, value in database.items() : 
        
            dist = np.linalg.norm(value-signature)
            if dist < min_dist:
                min_dist = dist
                identity = str(key)
        if min_dist>1:
                identity="unknown"
        if identity != "unkown" :
            if identity.isdigit():
                identity = int(identity)
            else:
                identity = None
            id_attendance.append(identity)
    #     font = cv2.FONT_HERSHEY_SIMPLEX
    #     font_scale = 0.5
    #     thickness = 1
    #     color = (0, 255, 0)
    #     text_size = cv2.getTextSize(identity, font, font_scale, thickness)[0]
    #     text_x = x1 + (x2 - x1) // 2 - text_size[0] // 2
    #     text_y = y1 - text_size[1] - 5
    #     cv2.putText(img, identity, (text_x, text_y), font, font_scale, color, thickness)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return id_attendance       