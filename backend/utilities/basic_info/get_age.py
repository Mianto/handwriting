import re
from ..jsonpreprocessor import get_first_name_box, get_adjacent_box


def age_printed(json_text):
    """
    Get the age if it is printed

    :param str json_text: text_description of the vision api
    """
    text = json_text.split('age')[1]
    li = re.findall(r"[0-9][0-9]", text)
    return li


def age_not_printed(json_text, first_name):
    """
    Get the age if it is not printed

    :param str json_text: text_description of the vision api
    :param str first_name: first name of the person
    """
    li = list()
    try:
        first_name_bb = get_first_name_box(json_dict, first_name)
        adjacent_first_name_boxes = get_adjacent_box(json_dict, first_name_bb)
        
        for box in adjacent_first_name_boxes:
            if re.match(r"[1-9][0-9]", box['description']):
                a = re.match(r"[1-9][0-9]",box['description'])
                li.append(''.join(a[0]))
            
    except Exception as e:
        return None


def validate_age(li):
    if li:
        for num in li:
            if 1 <= int(num) <= 100:
                return num
    return None


def age(json_dict, first_name=None):
    """
    :param dict json_dict: full response of the vision api in dict
    :param string first_name: first name of the patient
    :return int: Age if it exists
    """
    text = json_dict['textAnnotations'][0]['description']
    
    text.lower()
    if 'age' in text:
        # find age in case of printed
        li = age_printed(text)
        return validate_age(li)

    else:
        text = text.split(' ')
         
        if not first_name:
            return None

        li = age_not_printed(text, first_name)
        return validate_age(li)
            

if __name__ == "__main__":
    pass