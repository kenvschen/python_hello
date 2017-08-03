# usr/bin/env python3
# -*- coding: utf-8 -*-
# demo3
# This is a _very simple_ example of a web service that recognizes faces in uploaded images.

import face_recognition
import json
from PIL import Image
from flask import Flask, jsonify, request, redirect, Response, make_response
from flask_cors import *

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app, supports_credentials=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadImage', methods=['POST',''])
def upload_image():
    # Check if a valid image file was uploaded
    resp = Response("Foo bar baz")
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            # resp.data = find_faces_in_image(file)
            # return Response(json.dumps(find_faces_in_image(file)),
            #             # content_type=data.content_type,
            #             headers={
            #                 'Accept': '*/*',
            #                 'Access-Control-Allow-Origin': '*'
            #             })
           	return Response(json.dumps(find_faces_in_image(file)))

def find_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)

    # Find all the faces in the image
    face_locations = face_recognition.face_locations(img)

    face_landmarks_list = face_recognition.face_landmarks(img)

    # print("I found {} face(s) in this photograph.".format(len(face_locations)))
    facelist = list() 
    face_featureslist = list()

    for face_location in face_locations:

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        facelist.append({"top" : top, "right" : right, "bottom" : bottom, "left" : left})

    for face_landmarks in face_landmarks_list:
        facemarkslist = list()

        # Print the location of each facial feature in this image
        facial_features = [
            'chin',
            'left_eyebrow',
            'right_eyebrow',
            'nose_bridge',
            'nose_tip',
            'left_eye',
            'right_eye',
            'top_lip',
            'bottom_lip'
        ]

        # for facial_feature in facial_features:
            # print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

        # Let's trace out each facial feature in the image with a line!
        # pil_image = Image.fromarray(img)
        # d = ImageDraw.Draw(pil_image)

        for facial_feature in facial_features:
            # d.line(face_landmarks[facial_feature], width=2)
            facemarkslist.append({"%s" % facial_feature : face_landmarks[facial_feature]})

        face_featureslist.append(facemarkslist)

        # pil_image.show()

    # Get face encodings for any faces in the uploaded image
    # unknown_face_encodings = face_recognition.face_encodings(img)

    # face_found = False

    # if len(unknown_face_encodings) > 0:
    #     face_found = True

    # Return the result as json
    result = {
        # "face_found_in_image": face_found,
    	"facelist": facelist,
        "facemarkslist": face_featureslist
    }
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)