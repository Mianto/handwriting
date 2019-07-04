import json
import os
from pathlib import Path
import urllib.request
import configparser
from backend.utilities.jsonpreprocessor import dict_from_json
from backend.vision_api.request_json import request_json
from backend.utilities.basic_info import get_date, get_contact_number, get_name, get_age, get_gender


config = configparser.ConfigParser()
config.read('config.ini')
stanford_nlp_path = config['DEFAULT']['stanford-core-nlp']
name_file_path = config['DEFAULT']['name-list']
upload_folder = config['TEST']['upload_folder']
google_secret_key = config['DEFAULT']['GOOGLE_APPLICATION_CREDENTIALS']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_secret_key


def final_pipeline(blank_url, written_url):
    """
    :param Path image_folder: folder in which image is uploaded
    :param str written_image_name: actual prescription
    :param str blank_image_name: blank precription
    """
    # image_folder = Path(image_folder)
    # written_image_name =  image_folder / written_image_name
    # blank_image_name = image_folder / blank_image_name
    # create_new_folder(upload_folder)
    global upload_folder
    saved_blank_path = os.path.join(upload_folder, 'bl1.jpg')
    urllib.request.urlretrieve(blank_url, saved_blank_path)

    upload_folder = Path(upload_folder)

    blank_image_name = upload_folder / 'bl1.jpg'
    saved_written_path = os.path.join(upload_folder, 'wr1.jpg')
    written_image_name = upload_folder / 'wr1.jpg'
    urllib.request.urlretrieve(written_url, saved_written_path)

    blank_di = dict_from_json(request_json(blank_image_name))
    written_di = dict_from_json(request_json(written_image_name))

    name = get_name.name(written_di, name_file_path, stanford_nlp_path, blank_di)

    contact_written_number = get_contact_number.contact_number(written_di)
    contact_blank_number = get_contact_number.contact_number(blank_di)
    patient_contact = get_contact_number.patient_contact_number(contact_written_number, contact_blank_number)

    date = get_date.get_date_list(written_di)

    age = get_age.age(written_di, name[0])
    if type(name) == tuple:
        for n in name:
            if get_gender.gender(written_di, n):
                gender = get_gender.gender(written_di, n)
            if get_age.age(written_di, n):
                age = get_age.age(written_di, n)
    else:
        gender = get_gender.gender(written_di, name)
        age = get_age.age(written_di, name)

    basic_info = {'name': name, 'contact_number': patient_contact, 'date': date, 'age': age, 'gender': gender}

    basic_info = json.dumps(basic_info)
    print(basic_info)
    return basic_info


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath