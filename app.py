from flask import Flask, url_for, request
import logging
from flask_cors import CORS
import os
from werkzeug import secure_filename

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
    app.logger.info(PROJECT_HOME)
    if request.method == "POST" and request.files['image']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        create_new_folder(app.config['TEMP_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        # result = final_pipeline(app.config['UPLOAD_FOLDER'], img_name)
        return jsonify(
            result = result
        )
    else:
        return Response("No Image Sent", status=401)
        


