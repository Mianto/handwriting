import re
from jsonpreprocessor import get_first_name_box, get_adjacent_box


def age(json_dict, first_name):
    """
    :param dict json_dict: full response of the vision api in dict
    :param string first_name: first name of the patient
    :return int: Age if it exists
    """
    first_name_bb = get_first_name_box(json_dict, first_name)
    adjacent_first_name_boxes = get_adjacent_box(json_dict, first_name_bb)
    li = []
    text = json_dict['textAnnotations'][0]['description'].split(' ')
    i = 0
    # find age in case of printed
    for txt in text:
        i += 1
        if txt.lower() == 'age' or 'age' in txt.lower():
            while i < 100:
                if re.match(r"[0-9+]+", text[i + 1]):
                    return text[i + 1]
                i += 1
    
    # find age in case age not printed
    for box in adjacent_first_name_boxes:
        if re.match(r"^[0-9+]+", box['description']):
            li.append(box['description'])
    for num in li:
        if  '+' in num:
            return num
        elif 1 <= int(num) < 100:
            return num

    return None

if __name__ == "__main__":
    pass