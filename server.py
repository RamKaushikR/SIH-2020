from flask import Flask, request, jsonify
import VoiceRecognition
import FaceRecognition
import os


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
    file = request.files['filename']
    speaker = requests.form['speaker']

    file.save('VoiceRecognition/predict/file.wav')

    vr = VoiceRecognition.identify.Identify(source = 'predict/')
    result = vr.identify_speaker()
    
    match = 0
    
    if result == speaker:
        match = 1

    r = {'result': match}
    return jsonify(r)

@app.route('/addSpeaker', methods = ['GET', 'POST'])
def addSpeaker():
    file1 = request.files['filename1']
    file2 = request.files['filename2']
    file3 = request.files['filename3']
    file4 = request.files['filename4']
    file5 = request.files['filename5']
    speaker = request.form['speaker']
    
    file1.save('VoiceRecognition/speakers/file1.wav')
    file2.save('VoiceRecognition/speakers/file2.wav')
    file3.save('VoiceRecognition/speakers/file3.wav')
    file4.save('VoiceRecognition/speakers/file4.wav')
    file5.save('VoiceRecognition/speakers/file5.wav')
    
    vr = VoiceRecognition.speaker.Speakers()
    vr.add_speaker(speaker)

    r = {'result': 'Added Speaker'}
    return jsonify(r)

@app.route('/updateSpeaker', methods = ['GET', 'POST'])
def updateSpeaker():
    file = request.files['filename']
    speaker = request.form['speaker']
    
    file.save('VoiceRecognition/speakers/file1.wav')
    
    vr = VoiceRecognition.speaker.Speakers()
    vr.update_speaker(speaker)

    r = {'result': 'Updated Speaker'}
    return jsonify(r)

@app.route('/removeSpeaker', methods = ['GET', 'POST'])
def removeSpeaker():
    speaker = request.form['speaker']
    
    vr = VoiceRecognition.speaker.Speakers()
    vr.remove_speaker(speaker)

    r = {'result': 'Remove Speaker'}
    return jsonify(r)

@app.route('/findFace', methods = ['GET','POST'])
def findFace():
    #process the image here.. Need to get specification from KabishQ
    img = request.files['image']
    target = request.form['target']
    
    img.save('FaceRecognition/predict/img.jpg')

    fr = FaceRecognition.identify.Identify(source = 'predict/')
    result = fr.identify_face()
    
    match = 0
    
    if(result == target):
        match = 1
        
    r = {'result':match}
    return jsonify(r)

@app.route('/addFace', methods = ['GET', 'POST'])
def addFace():
    img = request.files['image']
    target = request.form['target']
    
    img.save('FaceRecognition/faces/img.jpg')

    fr = FaceRecognition.face.Face()
    fr.add_face(target)

    r = {'result': 'Added Face'}
    return jsonify(r)

@app.route('/updateFace', methods = ['GET', 'POST'])
def updateFace():
    img = request.files['image']
    target = request.form['target']
    
    img.save('FaceRecognition/faces/img.jpg')

    fr = FaceRecognition.face.Face()
    fr.update_face(target)

    r = {'result': 'Updated Face'}
    return jsonify(r)

@app.route('/deleteFace', methods = ['GET', 'POST'])
def deleteFace():
    target = request.form['target']
    
    fr = FaceRecognition.face.Face()
    fr.delete_face(target)

    r = {'result': 'Removed Face'}
    return jsonify(r)
