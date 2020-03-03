import os, io
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify, send_file, make_response
import base64
from werkzeug.utils import secure_filename
import cv2
import numpy as np

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_per(X,P):
	return 1-(X/P)


def rec_faces(files,p1,p2):
	max_x = 1000
	max_y = 600
	net = cv2.dnn.readNetFromCaffe(p1, p2)
	faces = []
	mx=0
	my=0
	num_faces=0
	f_ims = []
	im=0
	for f_path in files:
		image = cv2.imread(f_path)
		(h, w) = image.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
			(300, 300), (104.0, 177.0, 123.0))
		net.setInput(blob)
		detections = net.forward()
		det_locations = []

		if(detections.shape[2]!=0):
			for i in range(0,detections.shape[2]):
				if detections[0, 0, i, 2] > 0.5:
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					box = box.astype("int")
					box = np.append(box,[abs(box[0]-box[2]),abs(box[1]-box[3])])
					det_locations.append(box.astype('int'))
	
			det_locations = np.array(det_locations)
			if(det_locations.shape[0]!=0):
				faces.append(det_locations)
				num_faces+=det_locations.shape[0]
				maxs = np.amax(det_locations,axis=0)
				if maxs[5]>my:
					my = maxs[5]
				if maxs[4]>mx:
					mx = maxs[4]
				f_ims.append(im)
		im+=1

	if num_faces!=0:
		collage = np.zeros((my,mx*num_faces,3))
		faces = np.array(faces)
		k=0
		for f in range(0,faces.shape[0]):
			image = cv2.imread(files[f_ims[f]])
		
			for i in range(0, faces[f].shape[0]):
				p = image[faces[f][i][1]:faces[f][i][3],faces[f][i][0]:faces[f][i][2]]

				collage[:faces[f][i][5],k*maxs[4]:k*maxs[4]+faces[f][i][4]] = p
				k+=1
	
		sp = max(find_per(max_y,collage.shape[0]),find_per(max_x,collage.shape[1]))
		wb = int(collage.shape[1] *(1-sp))
		hb = int(collage.shape[0] *(1-sp))
		collage = cv2.resize(collage, (wb,hb),interpolation = cv2.INTER_AREA)

		cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "collage.jpg"),collage)
		return 1
	else:
		return 0



@app.route('/createCollage', methods=['POST','GET'])
def upload_file():
	if request.method == 'POST':
		files = request.files.getlist('files')
		f_paths = []
		for f in files:
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			f_paths.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		f_paths = np.array(f_paths)
		p = rec_faces(f_paths,app.config['MODEL_STRUCTURE'],app.config['MODEL_WEIGHTS'])
			
		byte_io = io.BytesIO()
		if(p==1):
			with open(os.path.join(app.config['UPLOAD_FOLDER'], "collage.jpg"),'rb') as f:
				byte_io.write(f.read())
		else:
			with open(os.path.join(app.config['UPLOAD_FOLDER'], "ff.jpg"),'rb') as f:
				byte_io.write(f.read())
		byte_io.seek(0)
		for f in f_paths:
			os.remove(f)
		resp = make_response(send_file(byte_io,mimetype='image/jpg'))
		resp.headers['Content-Transfer-Encoding']='base64'
		resp.status_code = 201
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp
	else:
		return "<h1><center> YO!</center></h1>"

if __name__ == "__main__":
    app.run(debug = True)
