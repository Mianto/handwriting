import re
from ..jsonpreprocessor import get_first_name_box, get_adjacent_box


def age(json_dict, first_name):
    """
    :param dict json_dict: full response of the vision api in dict
    :param string first_name: first name of the patient
    :return int: Age if it exists
    """
    if not first_name:
        return None
    first_name_bb = get_first_name_box(json_dict, first_name)
    adjacent_first_name_boxes = get_adjacent_box(json_dict, first_name_bb)
    li = []
    text = json_dict['textAnnotations'][0]['description'].split(' ')
    i = 0
    # find age in case of printed
    for txt in text:
        i += 1
        if txt.lower() == 'age' or 'age' in txt.lower():
            for _ in range(10):
                if re.match(r"^[1-9][0-9]", text[i]):
                    a = re.match(r"^[1-9][0-9]", text[i])
                    return ''.join(a[0])
                i += 1
    
    # find age in case age not printed
    for box in adjacent_first_name_boxes:
        if re.match(r"^[1-9][0-9]", box['description']):
            a = re.match(r"^[1-9][0-9]",box['description'])
            li.append(''.join(a[0]))
            
    for num in li:
        if  '+' in num:
            return num
        elif 1 <= int(num) < 100:
            return num

    return None

if __name__ == "__main__":
    pass