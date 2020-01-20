from flask import Flask, request, jsonify
from VoiceRecognition.identify import Voice_Identify
from VoiceRecognition.speaker import Speakers
from FaceRecognition.identify import Face_Identify
from FaceRecognition.face import Face
import os
import sksound
import time


directories = os.listdir('VoiceRecognition')

if 'speakers' not in directories:
    os.mkdir('VoiceRecognition/speakers')

if 'predict' not in directories:
    os.mkdir('VoiceRecognition/predict')

directories = os.listdir('FaceRecognition')

if 'faces' not in directories:
    os.mkdir('FaceRecognition/faces')

if 'predict' not in directories:
    os.mkdir('FaceRecognition/predict')

app = Flask(__name__)

@app.route('/findSpeaker', methods = ['GET', 'POST'])
def findSpeaker():
    result = None
    file = request.files['audio_file']
    speaker = request.form['speaker']
    print(speaker)

    file.save('predict/file.wav')
    print('Received file')

    vr = Voice_Identify(source = 'predict/')
    result = vr.identify_speaker()
    print(result)
    
    match = 0
    
    if result == speaker:
        match = 1

    r = {'result': match}
    return jsonify(r)

@app.route('/addSpeaker', methods = ['GET', 'POST'])
def addSpeaker():
    file = request.files['audio_file']
    speaker = request.form['speaker']

    file.save('speakers/file.mp3')
    file = sksound.sounds.Sound('speakers/file.mp3')
    file.write_wav('speakers/file.wav')
    print(os.listdir('speakers'))
    if 'file.mp3' in os.listdir('speakers'):
        os.remove('speakers/file.mp3')
    print(os.listdir('speakers'))
    
    vr = Speakers()
    vr.add_speaker(speaker)

    r = {'result': 'Added Speaker'}
    time.sleep(2)
    return jsonify(r)

@app.route('/updateSpeaker', methods = ['GET', 'POST'])
def updateSpeaker():
    file = request.files['audio_file']
    speaker = request.form['speaker']
    
    file.save('speakers/file.wav')
    
    vr = Speakers()
    vr.update_speaker(speaker)

    r = {'result': 'Updated Speaker'}
    return jsonify(r)

@app.route('/removeSpeaker', methods = ['GET', 'POST'])
def removeSpeaker():
    speaker = request.form['speaker']
    
    vr = Speakers()
    vr.remove_speaker(speaker)

    r = {'result': 'Remove Speaker'}
    return jsonify(r)

@app.route('/findFace', methods = ['GET','POST'])
def findFace():
    #process the image here.. Need to get specification from KabishQ
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('predict/img.jpg')
    print('Received File')

    fr = Face_Identify(source = 'predict/')
    result = fr.identify_face()
    print(result)
    
    match = 0
    
    if(result == target):
        match = 1
        
    r = {'result':match}
    return jsonify(r)

@app.route('/addFace', methods = ['GET', 'POST'])
def addFace():
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('faces/img.jpg')

    fr = Face()
    fr.add_face(target)

    r = {'result': 'Added Face'}
    return jsonify(r)

@app.route('/updateFace', methods = ['GET', 'POST'])
def updateFace():
    img = request.files['face_image']
    target = request.form['target']
    
    img.save('faces/img.jpg')

    fr = Face()
    fr.update_face(target)

    r = {'result': 'Updated Face'}
    return jsonify(r)

@app.route('/removeFace', methods = ['GET', 'POST'])
def removeFace():
    target = request.form['target']
    
    fr = Face()
    fr.remove_face(target)

    r = {'result': 'Removed Face'}
    return jsonify(r)
