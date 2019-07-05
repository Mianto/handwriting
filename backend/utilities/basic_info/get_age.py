import re
from ..jsonpreprocessor import box_within_percentage, get_text_from_bounding_box


def age_printed(json_text):
    """
    Get the age if it is printed

    :param str json_text: text_description of the vision api
    """
    text = json_text.split('age')[1]
    li = re.search(r"([1-9][0-9])", text[0:10])
    if li:
        return li.group(1)
    return None


def age_not_printed(json_dict, first_name):
    """
    Get the age if it is not printed

    :param str json_text: text_description of the vision api
    :param str first_name: first name of the person
    """
    li = list()
    try:
        texts = json_dict['textAnnotations'][0]['description'].split(' ')
        # first_name_bb = get_first_name_box(json_dict, first_name)
        # adjacent_first_name_boxes = get_adjacent_box(json_dict, first_name_bb)
        # # text = get_text_from_bounding_box(box_within_percentage(json_dict))
        
        # for box in adjacent_first_name_boxes:
        #     if re.match(r"[1-9][0-9]", box['description']):
        #         a = re.match(r"[1-9][0-9]",box['description'])
        #         li.append(''.join(a[0]))
        n = len(texts)
        for i, txt in enumerate(texts):
            if txt == first_name:
                break
            
        count = 0
        while count < 10:
            if len(text[i]) < 3:
                m1 = re.match(r"([1-9][0-9])", texts[i])
                if m1:
                    return m1.group(1)
            count += 1
            i += 1
    except Exception as e:
        return None


def validate_age(li):
    if 1 <= int(li) <= 100:
        return li
    return None


def age(json_dict, first_name=None):
    """
    :param dict json_dict: full response of the vision api in dict
    :param string first_name: first name of the patient
    :return int: Age if it exists
    """
    text = json_dict['textAnnotations'][0]['description']
    
    text = text.lower()
    if 'age' in text:
        # find age in case of printed
        li = age_printed(text)
        return validate_age(li)

    else:
        text = text.split(' ')
         
        if not first_name:
            return None

        li = age_not_printed(json_dict, first_name)
        return validate_age(li)
            

if __name__ == "__main__":
    pass