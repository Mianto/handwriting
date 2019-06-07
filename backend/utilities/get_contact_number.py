import json
import re
import os


def contact_number(json_dict):
    """
    Extract contact number from the json_dict file
    :param json_dict 
    :return all present contact numbers 
    """
    number = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', json_dict)


def patient_contact_number(written_number, blank_number)
    """
    param: contacts number in prescribed, contacts number in blank page
    return: patient conatct number
    """
    for i in written_number:
        falg = 0
        for j in blank_number:
            if i == j:
                falg = 1
        if falg == 0:
            patient_contact_number.append(i)

    return patient_contact_number


if __name__ == "__main__":
    pass

