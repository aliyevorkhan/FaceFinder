import face_recognition
from flask import Flask, request, redirect, render_template, url_for
import cv2
import numpy as np
from PIL import Image
from base64 import b64encode
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

#routing for previous results page
@app.route('/previous')
def previous():
    #get current working directory path and concate static folder path
    #send list of images in static folder to front
    mypath = os.getcwd()+'/static'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return render_template("previous.html", files=onlyfiles)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'searchedFace' and 'groupFace' not in request.files:
            return redirect(request.url)

        searchedFace = request.files['searchedFace']
        groupFace = request.files['groupFace']

        if searchedFace.filename == '' or groupFace.filename == '':
            return redirect(request.url)

        if searchedFace and allowed_file(searchedFace.filename):
            # The image file seems valid! Detect faces and return the result.
            return recognition(searchedFace, groupFace)
        '''
        if groupFace and allowed_file(groupFace.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(groupFace)
        '''
    # If no valid image file was uploaded, show the file upload form:
    return render_template("index.html")

def recognition(searchedFace, groupFace):
    searchedFaceImg = face_recognition.load_image_file(searchedFace)
    searchedFaceEncoding = face_recognition.face_encodings(searchedFaceImg)[0]

    known_faces = [searchedFaceEncoding]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    
    groupFaceImg = Image.open(groupFace)
    groupFaceImg = np.array(groupFaceImg)
    groupFaceImg = cv2.cvtColor(np.array(groupFaceImg), cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the current groupFaceImg
    face_locations = face_recognition.face_locations(groupFaceImg)
    face_encodings = face_recognition.face_encodings(groupFaceImg, face_locations)

    faceConfidence = face_recognition.face_distance(face_encodings, searchedFaceEncoding)    
    count = 0
    
    for face_encoding in face_encodings:

        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        name = None
        color = (0,0,0)
        if match[0]:
            name = "searched"
        else:
            name = "other"

        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        if name=="searched":
            color = (0,0,255)
        else:
            color = (255,0,0)

        #similarity similarityScore
        similarityScore = str(int((1-faceConfidence[count])*100))

        # Draw a box around the face
        cv2.rectangle(groupFaceImg, (left, top), (right, bottom), color, 3)

        # Draw a label with a name below the face
        cv2.rectangle(groupFaceImg, (left, bottom - 40), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(groupFaceImg, similarityScore + " %", (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)
        count+=1

    cv2.imwrite("static/result" + datetime.utcnow().strftime('%B%d%Y%H%M%S') +".jpg", groupFaceImg)

    retval, buffer_img= cv2.imencode('.jpg', groupFaceImg)
    data = b64encode(buffer_img)

    return render_template("result.html", data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
