from flask import Flask
from flask_cors import CORS
import os


UPLOAD_FOLDER = r'/..\find_faces_api\load'

MODEL_STRUCTURE = r'/..\find_faces_api\model\deploy.prototxt.txt'
MODEL_WEIGHTS = r'/..\find_faces_api\model\res10_300x300_ssd_iter_140000.caffemodel'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MODEL_STRUCTURE'] = MODEL_STRUCTURE
app.config['MODEL_WEIGHTS'] = MODEL_WEIGHTS

CORS(app)