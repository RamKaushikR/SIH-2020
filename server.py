from flask import Flask, request, jsonify
from VoiceRecognition.identify import Voice_Identify
from VoiceRecognition.speaker import Speakers
from FaceRecognition.identify import Face_Identify
from FaceRecognition.face import Face
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import os
import sksound
import time
import numpy as np
import cv2
import imutils
import pickle
"""
for fakeness detection
"""
protoPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
modelPath = os.path.sep.join(["face_detector", "res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

print("[INFO] loading liveness detector...")
model = load_model("liveness.model")
le = pickle.loads(open("le.pickle", "rb").read())

"""
all necessary models loaded
"""

directories = os.listdir('./')

if 'speakers' not in directories:
    os.mkdir('speakers')

if 'predict' not in directories:
    os.mkdir('predict')

if 'faces' not in directories:
    os.mkdir('faces')

app = Flask(__name__)

@app.route('/findSpeaker', methods = ['GET', 'POST'])
def findSpeaker():
    result = 0

    file = request.files['audio_file']
    speaker = request.form['speaker']
    print('Speaker to be identified is ' + speaker)

    file.save('predict/file.mp3')
    #"""
    file1 = sksound.sounds.Sound('predict/file.mp3')
    file1.write_wav('predict/file.wav')
    os.remove('predict/file.mp3')
    #"""
    print('Received file')

    vr = Voice_Identify(source = 'predict/')
    result = vr.identify_speaker(speaker)
    print(result)
    """    
    match = 0
    
    if result == speaker:
        match = 1
    """
    r = {'result': result}
    return jsonify(r)

@app.route('/addSpeaker', methods = ['GET', 'POST'])
def addSpeaker():
    file1 = request.files['audio_file1']
    file2 = request.files['audio_file2']
    file3 = request.files['audio_file3']
    file4 = request.files['audio_file4']
    file5 = request.files['audio_file5']
    speaker = request.form['speaker']

    file1.save('speakers/file1.mp3')
    file2.save('speakers/file2.mp3')
    file3.save('speakers/file3.mp3')
    file4.save('speakers/file4.mp3')
    file5.save('speakers/file5.mp3')

    file1 = sksound.sounds.Sound('speakers/file1.mp3')
    file1.write_wav('speakers/file1.wav')
    file2 = sksound.sounds.Sound('speakers/file2.mp3')
    file2.write_wav('speakers/file2.wav')
    file3 = sksound.sounds.Sound('speakers/file3.mp3')
    file3.write_wav('speakers/file3.wav')
    file4 = sksound.sounds.Sound('speakers/file4.mp3')
    file4.write_wav('speakers/file4.wav')
    file5 = sksound.sounds.Sound('speakers/file5.mp3')
    file5.write_wav('speakers/file5.wav')

    try:
        os.remove('speakers/file1.mp3')
        os.remove('speakers/file2.mp3')
        os.remove('speakers/file3.mp3')
        os.remove('speakers/file4.mp3')
        os.remove('speakers/file5.mp3')
    except:
        pass
    
    vr = Speakers()
    result = vr.add_speaker(speaker)

    r = {'result': result}
    return jsonify(r)

@app.route('/updateSpeaker', methods = ['GET', 'POST'])
def updateSpeaker():
    file = request.files['audio_file']
    speaker = request.form['speaker']
    
    file.save('speakers/file.wav')
    
    vr = Speakers()
    result = vr.update_speaker(speaker)

    r = {'result': result}
    return jsonify(r)

@app.route('/removeSpeaker', methods = ['GET', 'POST'])
def removeSpeaker():
    speaker = request.form['speaker']
    
    vr = Speakers()
    result = vr.remove_speaker(speaker)

    r = {'result': result}
    return jsonify(r)

@app.route('/findFace', methods = ['GET','POST'])
def findFace():
    #process the image here.. Need to get specification from KabishQ
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('predict/img.jpg')
    print('Received File')

    fr = Face_Identify(source = 'predict/')
    result = fr.identify_face(target)
        
    r = {'result': result}
    return jsonify(r)

@app.route('/addFace', methods = ['GET', 'POST'])
def addFace():
    result = 0
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('faces/img.jpg')

    fr = Face()
    result = fr.add_face(target)

    r = {'result': result}
    return jsonify(r)

@app.route('/updateFace', methods = ['GET', 'POST'])
def updateFace():
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('faces/img.jpg')

    fr = Face()
    result = fr.update_face(target)

    r = {'result': result}
    return jsonify(r)

@app.route('/removeFace', methods = ['GET', 'POST'])
def removeFace():
    target = request.form['target']
    
    fr = Face()
    result = fr.remove_face(target)

    r = {'result': result}
    return jsonify(r)
