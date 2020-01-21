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
    result = 0
    file = request.files['audio_file']
    speaker = request.form['speaker']
    print('Speaker to be identified is ' + speaker)

    file.save('predict/file.wav')
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
    vr.add_speaker(speaker)

    r = {'result': 'Added Speaker'}
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
