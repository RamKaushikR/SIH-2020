from flask import Flask, request, jsonify
import VoiceRecognition
import FaceRecognition


app = Flask(__name__)

@app.route('/findSpeaker', methods = ['GET', 'POST'])
def findSpeaker():
    file = request.args.get('filename')
    speaker = request.args.get('speaker')
    
    file.write('VoiceRecognition/predict/file.wav')
    vr = VoiceRecognition.identify.Identify(source = 'predict/')
    result = vr.identify_speaker()
    
    match = 0
    
    if result == speaker:
        match = 1
    r = {'result': match}
    return jsonify(r)

@app.route('/addSpeaker', methods = ['GET', 'POST'])
def addSpeaker():
    file1 = request.args.get('filename1')
    file2 = request.args.get('filename2')
    file3 = request.args.get('filename3')
    file4 = request.args.get('filename4')
    speaker = request.args.get('speaker')
    
    file1.write('VoiceRecognition/speakers/file1.wav')
    file2.write('VoiceRecognition/speakers/file2.wav')
    file3.write('VoiceRecognition/speakers/file3.wav')
    file4.write('VoiceRecognition/speakers/file4.wav')
    
    vr = VoiceRecognition.speaker.Speakers()
    vr.add_speaker(speaker)

@app.route('/updateSpeaker', methods = ['GET', 'POST'])
def updateSpeaker():
    file1 = request.args.get('filename')
    speaker = request.args.get('speaker')
    
    file1.write('VoiceRecognition/speakers/file1.wav')
    
    vr = VoiceRecognition.speaker.Speakers()
    vr.update_speaker(speaker)

@app.route('/removeSpeaker', methods = ['GET', 'POST'])
def removeSpeaker():
    speaker = request.args.get('speaker')
    
    vr = VoiceRecognition.speaker.Speakers()
    vr.remove_speaker(speaker)

@app.route('/findFace', methods = ['GET','POST'])
def findFace():
    #process the image here.. Need to get specification from KabishQ
    img = request.args.get('image')
    target = request.args.get('target')
    
    img.write('FaceRecognition/predict/img.jpg')
    fr = FaceRecognition.identify.Identify(source = 'predict/')
    result = fr.identify_face()
    
    match = 0
    
    if(result == target):
        match = 1
        
    r = {'result':match}
    return jsonify(r)

@app.route('/addFace', methods = ['GET', 'POST'])
def addFace():
    img = request.args.get('image')
    target = request.args.get('target')
    
    img.write('FaceRecognition/faces/img.jpg')
    fr = FaceRecognition.face.Face()
    fr.add_face(target)

@app.route('/updateFace', methods = ['GET', 'POST'])
def updateFace():
    img = request.args.get('image')
    target = request.args.get('target')
    
    img.write('FaceRecognition/faces/img.jpg')
    fr = FaceRecognition.face.Face()
    fr.update_face(target)

@app.route('/deleteFace', methods = ['GET', 'POST'])
def deleteFace():
    target = request.args.get('target')
    
    fr = FaceRecognition.face.Face()
    fr.delete_face(target)
