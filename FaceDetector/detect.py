from keras.preprocessing.image import img_to_array
from keras.models import load_model
import os
import cv2
import sksound
import time
import numpy as np
import imutils
import pickle
import tensorflow as tf
"""
for fakeness detection
"""

def init():
    model = load_model('liveness.h5')
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    graph = tf.get_default_graph()
    return model, graph

protoPath = os.path.sep.join(['face_detector', 'deploy.prototxt'])
modelPath = os.path.sep.join(['face_detector', 'res10_300x300_ssd_iter_140000.caffemodel'])
net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
le = pickle.loads(open('le.pickle', 'rb').read())
model, graph = init()

def show(img):
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def isFake(path):
    """
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('predict/img.jpg')
    print('Received File for fake detection')
    """
    global net, model, le, graph

    frame = cv2.imread(path)
    frame = imutils.resize(frame, width = 600)
    #show(frame)

    (h, w) = frame.shape[: 2]

    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    result = -1

    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the face and extract the face ROI
            box = detections[0, 0, i, 3: 7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype('int')
            # ensure the detected bounding box does fall outside the
            # dimensions of the frame
            startX = max(0, startX)
            startY = max(0, startY)
            endX = min(w, endX)
            endY = min(h, endY)
            # extract the face ROI and then preproces it in the exac
            # same manner as our training data
            face = frame[startY: endY, startX: endX]
            face = cv2.resize(face, (64, 64))
            #show(cv2.resize(face.copy(), (256, 256)))
            face = face.astype('float') / 255.0
            face = img_to_array(face)
            face = np.expand_dims(face, axis = 0)

            # pass the face ROI through the trained liveness detector
            # model to determine if the face is 'real' or 'fake'
            with graph.as_default():
                preds = model.predict(face)[0]
                j = np.argmin(preds)
                label = le.classes_[j]

                # draw the label and bounding box on the frame
                verdict = label.decode('utf-8')
                if(verdict == 'real'):
                    result = 1
    return result
