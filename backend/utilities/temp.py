from ner.name_recognition import get_ner
import get_contact_number
from jsonpreprocessor import dict_from_json_file
from get_name import name
import copy
import get_date
import get_gender
import get_age

# data = dict_from_json(r'/home/prasahnt/Desktop/handwriting/backend/utilities/ner/resources')
# li = get_ner(data,r'/home/prasahnt/Dev/Gcloud/src/stanford-corenlp-full-2018-10-05')
# li1 = get_contact_number.contact_number(data)
# li2 = copy.copy(li1)
# li2.append('9002762888')

# print(get_contact_number.patient_contact_number(li2,li1))
total = dict_from_json_file('/home/prasahnt/Desktop/handwriting/backend/utilities/ner/resources/mandeep_yadav_written_clolr_180.json')
# blank = dict_from_json_file('/home/prasahnt/Desktop/handwriting/backend/utilities/ner/resources/mandeep_yadav_blank_color_0.json')
# name_list = '/home/prasahnt/Dev/Gcloud/src/name_updated_anuj_first_last.txt'
# core_nlp = '/home/prasahnt/Desktop/resources/stanford-corenlp-full-2018-10-05'
# print(name(total,blank,name_list,core_nlp)) 

print(get_date.get_date_list(total))
print(get_gender.gender_printed(total),get_age.age(total, "MANJU"))