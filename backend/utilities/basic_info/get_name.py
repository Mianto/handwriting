from ..ner.name_recognition import get_ner
from ..jsonpreprocessor import *


def get_first_name_if_name(json_dict, name_list):
    """
    Get the first name if Name is printed

    :param dict json_dict: full response of the vision api in dict
    :return first_name in case of printed name
    """
    texts = json_dict['textAnnotations'][0]['description']
    texts = texts.replace('\n', ' ')
    texts = texts.split(' ')
    i = 0
    for txt in texts:
        i += 1
        if txt.lower() == "name" or "name" in txt.lower():
            j = 0
            while len(texts[i]) < 2 and j < 50:
                i += 1
                j += 1
            if texts[i].lower() in name_list:
                return texts[i]
                
    return None


def is_name_present(json_dict):
    texts = json_dict['textAnnotations'][0]['description']
    if "name" in texts.lower():
        return True
    return False


def is_title_present(json_dict):
    texts = json_dict['textAnnotations'][0]['description']
    title_list = ['mr.', 'mr', 'mrs', 'mrs.', 'ms.', 'ms', 'miss']
    for title in title_list:
        if title in texts.lower():
            return True
    return False    


def get_vocab_terms(path):
    """
    Load file to a set

    :param str path: path to the file to be loaded
    :return set: A set containing all the names 
    """
    vocab = list()
    with open(path, "r") as fp:
        for i in fp:
            vocab.append(i.strip().lower())
    return set(vocab)


def get_title_if_present(json_dict, name_list):
    texts = get_text_from_bounding_box(box_within_percentage(json_dict))
    texts = texts.split(' ')
    title_list = ['mr.', 'mr', 'mrs', 'mrs.', 'ms.', 'ms', 'miss']
    n = len(texts)
    i = 0
    flag = 0
    while i < n:
        for title in title_list:
            if title in texts[i].lower():
                flag = 1
                break
        if flag == 1:
            break
        i += 1

    total_name = list()
    
    while i < n:
        w = texts[i].lower()
        if w in name_list:
            total_name.append(texts[i])
        i += 1

    if len(total_name) > 1:
        return tuple(total_name)
    elif len(total_name) == 1:
        return (total_name, )
    else:
        return None


def name(json_dict, name_list_path, core_nlp_path, json_dict_blank):
    """
    Get name if it exist in name vocab list

    :param dict json_dict: full response of the vision api in dict
    :param dict json_dict_blank: response of the blank page for the google api
    :param Path name_list_path: path of the name list of the file
    :param Path core_nlp_path: path of the stanford core nlp
    """
    if not json_dict:
        return None
    
    name_vocab = get_vocab_terms(path=name_list_path)

    if is_name_present(json_dict):
        first_name = get_first_name_if_name(json_dict, name_vocab)
        last_name = get_last_name(json_dict, first_name, name_vocab)
        if last_name: 
            return (first_name, last_name)
        return (first_name,)

    elif is_title_present(json_dict):
        return get_title_if_present(json_dict, name_vocab)

    else:
        if json_dict:
            total = get_ner(json_dict, core_nlp_path)
            
        if json_dict_blank:
            blank = get_ner(json_dict_blank, core_nlp_path)
            written = list(set(total) - set(blank))

        else:
            written = list(set(total))

        name_list = list()

        for word in written:
            if word.strip().lower() in name_vocab:
                name_list.append(word)
      
        for name in name_list:
            last_name = get_last_name(json_dict, name, name_vocab)

            if last_name:
                return (name, last_name)
        if len(name_list) > 0:
            return name_list[0]
        return None
    
    
def get_last_name(json_dict, first_name, name_list):
    # first name is either giving first name or last name
    # check one word before and after the name
    # boxes = get_adjacent_box(json_dict, get_first_name_box(json_dict, first_name), 0.005)
    # if boxes:
    #     for i in range(len(boxes)):
    #         if boxes[i]['description'].strip().lower() in name_list:
    #             return boxes[i]['description']
    texts = get_text_from_bounding_box(box_within_percentage(json_dict))
    texts = texts.split(' ')
    n = len(texts)
    for i, txt in enumerate(texts):
        if txt == first_name:
            break
    
    while i < n and i > 2:
        if texts[i - 2] != first_name and texts[i - 2].lower() in name_list:
            return texts[i - 2]
        i += 1
    return None

    






