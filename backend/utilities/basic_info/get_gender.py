from genderize import Genderize
from ..jsonpreprocessor import box_within_percentage, get_text_from_bounding_box


def get_gender_if_printed(json_dict):
    """
    Get the gender if gender is printed
    
    :param dict json_dict: full response of the vision api in dict
    :return first_name in case of printed name
    """
    gender_list = ['m', 'f', 'male', 'female']
    texts = get_text_from_bounding_box(box_within_percentage(json_dict))
    i = 0
    for txt in texts:
        i += 1
        if txt.lower() == 'gender' or "gender" in txt.lower() or "sex" in txt.lower() or txt.lower() == "sex":
            j = 0
            for gender_ele in gender_list:
                while gender_ele in texts[i].lower() and j < 10: 
                    i += 1
                    j += 1
            return texts[i]     
    return None


def get_gender_using_title(json_dict, first_name):
    """
    Get the gender using Titles Mr., Mrs., Miss (not using Ms clashing)
    
    :param dict json_dict: full response of the vision api in dict
    :return first_name in case of printed name
    """
    title_list = ['mr.', 'mr', 'mrs', 'mrs.', 'ms.', 'ms', 'miss']
    male_title_list = ['mr.', 'mr']
    female_title_list = ['mrs', 'mrs.', 'ms.', 'ms', 'miss']
    try:
        texts = get_text_from_bounding_box(box_within_percentage(json_dict))
        texts = texts.split(first_name)[:1]
        for txt in texts:
            for title in title_list:
                if title in txt.lower():
                    if title in male_title_list:
                        return 'M'
                    else:
                        return 'F'
        return False
    except Exception as e:
        return None


def check_for_gender(json_dict, first_name, initial_guess_list):
    # assumption gender is not written before name
    try:
        texts = get_text_from_bounding_box(box_within_percentage(json_dict))
        texts = texts.split(first_name)[1:]
        for txt in texts:  
            for guess in initial_guess_list:
                if guess in txt:
                    return True
        return False
    except Exception as e:
        return False


def gender(json_dict, first_name):
    """
    Get the gender of the patient

    :param dict json_dict: full response of the vision api in dict
    :param str first_name: first_name of the patients
    :return gender in case of printed gender
    """
    male_guess_list = ['M', 'Male', 'm']
    female_guess_list = ['F', 'Female', 'f']

    gender_printed = get_gender_if_printed(json_dict)
    if gender_printed:
        if gender_printed == 'm' or gender_printed == 'male':
            return 'M'
        elif gender_printed == 'f' or gender_printed == 'female':
            return 'F'

    title_gender = get_gender_using_title(json_dict, first_name)
    if title_gender:
        return title_gender
    
    try:
        li = Genderize().get([first_name])[0]
        if li['gender'] == 'male':
            if check_for_gender(json_dict, first_name, male_guess_list):
                return "M"
        elif li['gender'] == 'female':
            if check_for_gender(json_dict, first_name, female_guess_list):
                return "F"
        return None
    
    except Exception as e:
        print("Genderize not responding {}".format(e))
        return None

if __name__ == "__main__":
    pass