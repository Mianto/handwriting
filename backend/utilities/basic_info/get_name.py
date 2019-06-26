from ..ner.name_recognition import get_ner
from ..jsonpreprocessor import *


def get_first_name_if_name(json_dict):
    """Get the first name if Name is printed
    :param dict json_dict: full response of the vision api in dict
    :return first_name in case of printed name
    """
    texts = json_dict['textAnnotations'][0]['description'].split(' ')
    i = 0
    for txt in texts:
        i += 1
        if txt.lower() == 'name' or "name" in txt.lower():
            j = 0
            while len(texts[i]) < 2 and j < 50:
                i += 1
                j += 1
            return texts[i]
                
    return None


def is_name_present(json_dict):
    texts = json_dict['textAnnotations'][0]['description'].split(' ')
    if "name" in texts or "Name" in texts or "Name:" in texts:
        return True
    return False


def get_vocab_terms(path):
    """Load file to a set
    :param str path: path to the file to be loaded
    :return set: A set containing all the names 
    """
    vocab = list()
    with open(path, "r") as fp:
        for i in fp:
            vocab.append(i.strip().lower())
    return set(vocab)


def name(json_dict, name_list_path, core_nlp_path, json_dict_blank):
    """Get name if it exist in name vocab list
    :param dict json_dict: full response of the vision api in dict
    :param dict json_dict_blank: response of the blank page for the google api
    :param Path name_list_path: path of the name list of the file
    :param Path core_nlp_path: path of the stanford core nlp
    """
    if not json_dict:
        return None
    
    name_vocab = get_vocab_terms(path=name_list_path)

    if is_name_present(json_dict):
        first_name = get_first_name_if_name(json_dict)
        last_name = get_last_name(json_dict, first_name, name_vocab)
        if last_name: 
            return (first_name, last_name)
        return first_name

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
        return name_list[0]
    
    
def get_last_name(json_dict, first_name, name_list):
    boxes = get_adjacent_box(json_dict, get_first_name_box(json_dict, first_name), 0.005)
    if boxes:
        for i in range(len(boxes)):
            if boxes[i]['description'].strip().lower() in name_list:
                return boxes[i]['description']

    






