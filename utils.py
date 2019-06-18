import json
from pathlib import Path
from backend.utilities.jsonpreprocessor import dict_from_json
from backend.vision_api.request_json import request_json
from backend.utilities.basic_info import get_date, get_contact_number, get_name, get_age, get_gender


def final_pipeline(image_folder, written_image_name, blank_image_name):
    """
    :param Path image_folder: folder in which image is uploaded
    :param str written_image_name: actual prescription
    :param str blank_image_name: blank precription
    """
    image_folder = Path(image_folder)
    written_image_name =  image_folder / written_image_name
    
    blank_image_name = image_folder / blank_image_name
    print(written_image_name, blank_image_name)

    blank_di = dict_from_json(request_json(blank_image_name))
    written_di = dict_from_json(request_json(written_image_name))
    
    name = get_name.name(written_di, r"backend\vision_api\resources\name_list.txt", r"backend\vision_api\resources\stanford-corenlp-full-2018-10-05", blank_di)
    contact_written_number = get_contact_number.contact_number(written_di)
    contact_blank_number = get_contact_number.contact_number(blank_di)
    patient_contact = get_contact_number.patient_contact_number(contact_written_number, contact_blank_number)
    date = get_date.get_date_list(written_di)
    age = get_age.age(written_di, name[0])
    gender = get_gender.gender(name[0])

    basic_info = {'name': name, 'contact_number': patient_contact, 'date': date, 'age': age, 'gender': gender}

    basic_info = json.dumps(basic_info)
    print(basic_info)
    return json.loads(basic_info)



