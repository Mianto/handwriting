'''
set environment variable in conda environment
    mkdir -p ./etc/conda/activate.d
    mkdir -p ./etc/conda/deactivate.d
    touch ./etc/conda/activate.d/env_vars.sh
    touch ./etc/conda/deactivate.d/env_vars.sh
In activate.d/env_vars.sh
    export GOOGLE_APPLICATION_CREDENTIALS="credential path"
In activate.d/env_vars.sh
    unset GOOGLE_APPLICATION_CREDENTIALS
In en
'''

import io
import os
import google.cloud
import json
from google.protobuf.json_format import MessageToJson
from google.cloud import vision

def request_json (path):
    """
    :param str path - Jpg image path
    :return str(Json) file recieved from google cloud vision api
    """
    # call vision api
    try:
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.document_text_detection(image=image)

        response = MessageToJson(response)
        return response

    except Exception as e:
        print("Vision API failed to make any response" + e)
    
if __name__ == "__main__":
    pass