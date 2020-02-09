from flask import Flask, request, jsonify
from VoiceRecognition.identify import Voice_Identify
from VoiceRecognition.speaker import Speakers
from FaceRecognition.identify import Face_Identify
from FaceRecognition.face import Face
from FaceDetector.detect import isFake
import os
import sksound
import numpy as np
import cv2


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

    file.save('predict/file.wav')
    print('Received file')

    vr = Voice_Identify(source = 'predict/')
    result = vr.identify_speaker(speaker)
    print(result)

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

    file1.save('speakers/file1.wav')
    file2.save('speakers/file2.wav')
    file3.save('speakers/file3.wav')
    file4.save('speakers/file4.wav')
    file5.save('speakers/file5.wav')
    
    vr = Speakers()
    result = vr.add_speaker(speaker)
    print(result)

    r = {'result': result}
    return jsonify(r)

@app.route('/updateSpeaker', methods = ['GET', 'POST'])
def updateSpeaker():
    file = request.files['audio_file']
    speaker = request.form['speaker']
    
    file.save('speakers/file.wav')
    
    vr = Speakers()
    result = vr.update_speaker(speaker)
    print(result)

    r = {'result': result}
    return jsonify(r)

@app.route('/removeSpeaker', methods = ['GET', 'POST'])
def removeSpeaker():
    speaker = request.form['speaker']
    
    vr = Speakers()
    result = vr.remove_speaker(speaker)
    print(result)

    r = {'result': result}
    return jsonify(r)

@app.route('/findFace', methods = ['GET','POST'])
def findFace():
    #process the image here.. Need to get specification from KabishQ
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('predict/img.jpg')
    print('Received File')

    
    real = isFake('predict/img.jpg')

    if real == -1:
        result = -1
    else:
    
        fr = Face_Identify(source = 'predict/')
        result = fr.identify_face(target)
    print(result)
        
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
    print(result)

    r = {'result': result}
    return jsonify(r)

@app.route('/updateFace', methods = ['GET', 'POST'])
def updateFace():
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('faces/img.jpg')

    fr = Face()
    result = fr.update_face(target)
    print(result)

    r = {'result': result}
    return jsonify(r)

@app.route('/removeFace', methods = ['GET', 'POST'])
def removeFace():
    target = request.form['target']
    
    fr = Face()
    result = fr.remove_face(target)
    print(result)

    r = {'result': result}
    return jsonify(r)
