from flask import Flask, url_for, request, Response, jsonify
import logging
from flask_cors import CORS
import os
from werkzeug import secure_filename
from utils import final_pipeline


written_url = "https://jrcdn.azureedge.net/justreliefblob/Lab/4084/2019/6/27/636972560515071077.jpg"
blank_url = "https://jrcdn.azureedge.net/justreliefblob/Lab/4084/2019/6/27/636972561000886436.jpg"

app = Flask(__name__)
CORS(app)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/input_images'.format(PROJECT_HOME)
TEMP_FOLDER = '{}/temp_images'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMP_FOLDER'] = TEMP_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


@app.route('/upload', methods = ['POST'])
def api_root():
    try:
        uploaded_files = request.files.getlist('file[]')
        file_names = []
        create_new_folder(app.config['UPLOAD_FOLDER'])
        
        for img in uploaded_files:
            img_name = secure_filename(img.filename)
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            img.save(saved_path)
            file_names.append(img_name)
        

        result = final_pipeline(app.config['UPLOAD_FOLDER'], file_names[0], file_names[1])
        return jsonify(result)

   
    except:
        return Response("No Image Sent", status=401)
    
if __name__ == "__main__":
    app.run(debug=True)


