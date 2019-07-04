import json
import re
import os


def contact_number(json_dict):
    """
    Extract contact number from the json_dict file
    :param json_dict 
    :return all present contact numbers 
    """
    try:
        li = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', json_dict['textAnnotations'][0]['description'])
        return ten_digit_contact_number(li)
    
    except Exception as e:
        print ("Exception" + str(e))
        return []


def remove_space(li):
    for x in li:
        x.replace(" ", "")
    return li


def ten_digit_contact_number(li):
    ret_li = []
    for x in li:
        if len(x) == 10:
            ret_li.append(x)
    return ret_li


def patient_contact_number(written_number, blank_number):
    """
    param: contacts number in prescribed, contacts number in blank page
    return: patient conatct number
    """
    if blank_number and written_number:
       li = list(set(written_number) - set(blank_number))
       # li = remove_space(li)
       return li
    return written_number


if __name__ == "__main__":
    pass

