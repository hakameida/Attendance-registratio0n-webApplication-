from PIL import Image
from numpy import asarray
from numpy import expand_dims


import pickle

import cv2

def makePkl(a, model , model_yolo ) :
    database = {}
    listIdPath=list(a.items())
    for id,path in listIdPath : 
        print(path)
        gbr1 = cv2.imread(path)
        img = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        results = model_yolo.predict(source=img)
        faces=results[0].boxes.xyxy
        x1,y1,x2,y2=faces[0]
        x1=int(x1)
        y1=int(y1)
        x2=int(x2)
        y2=int(y2)
        gbr = Image.fromarray(img) 
        gbr_array = asarray(gbr)
        face = gbr_array[y1:y2, x1:x2]                        
        face = Image.fromarray(face)                       
        face = face.resize((160,160))
        face = asarray(face)
        face = expand_dims(face, axis=0)
        signature = model.embeddings(face)
        
        database[id]=signature
    myfile = open("data4.pkl", "wb")
    pickle.dump(database, myfile)
    myfile.close()
    print("finish making pkl")
    return myfile 

        