import json
from utilities.jsonpreprocessor import dict_from_json
from vision_api.request_json import request_json
from utilities.basic_info import get_date, get_contact_number, get_name, get_age, get_gender


def final_pipeline(image_folder, written_image_name, blank_image_name):
    """
    :param Path image_folder: folder in which image is uploaded
    :param str written_image_name: actual prescription
    :param str blank_image_name: blank precription
    """

    blank_di = dict_from_json(request_json(blank_image_name))
    written_di = dict_from_json(request_json(written_image_name))

    name = get_name.name(written_di, blank_di)
    contact_number = get_contact_number.contact_number(written_di)
    patient_contact = get_contact_number.patient_contact_number(written_di, blank_di)
    date = get_date.get_date_list(written_di)
    age = get_age.age(written_di)
    gender = get_gender.gender_printed(written_di)

    basic_info = {'name': name, 'contact_number': patient_contact, 'date': date, 'age': age, 'gender': gender}

    basic_info = json.dumps(basic_info)
    
    return json.loads(basic_info)



