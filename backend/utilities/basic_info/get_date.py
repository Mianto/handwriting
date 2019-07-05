import re
from dateutil.parser import parse
import datetime


def get_date_list(json_dict):
    """
    Get date list from the page containing both current date and followup date
    
    :param dict json_dict: full response of the vision api in dict
    :return date in datetime format
    """
    date_list = list()
    date_list_str = list()
    texts = json_dict['textAnnotations'][0]['description'].replace('\n', ' ')
    texts = texts.split(' ')
    for txt in texts:
        # format -> 31/1/2019 or or 31-1-2019
        match1 = re.search(r"(0?[1-9]|[12][0-9]|3[01])[1\/\-](0?[1-9]|1[012])[1\/\-](\d{4})", txt)
        # format -> 31/1/19 or or 31-1-19
        match2 = re.search(r"(0?[1-9]|[12][0-9]|3[01])[1\/\-](0?[1-9]|1[012])[1\/\-](\d{2})", txt)
        # format -> 31/May/2019
        match3 = re.search(r"(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}(st|nd|rd|th)?)?(([ ,.\-\/])\D?)?((19[7-9]\d|20\d{2})|\d{2})*", txt)
        
        if match1:
            if is_date(match1.group(), fuzzy=True):
                date_list.append(is_date(match1.group(), fuzzy=True))
            else:
                # 1 is present in b/w dates
                date_temp_with_one = match1.group(1) + '/' + match1.group(2) + '/' +match3.group(3)
                if is_date(date_temp_with_one, fuzzy=True):
                    date_list.append(is_date(date_temp_with_one, fuzzy=True))
        if match2:
            if is_date(match2.group(), fuzzy=True):
                date_list.append(is_date(match2.group(), fuzzy=True))
        
            else:
                # 1 is present in b/w dates
                date_temp_with_one = match1.group(1) + '/' + match1.group(2) + '/' +match3.group(3)
                if is_date(date_temp_with_one, fuzzy=True):
                    date_list.append(is_date(date_temp_with_one, fuzzy=True))
                    
        if match3:
            if is_date(match3.group(), fuzzy=True):
                date_list.append(is_date(match3.group(), fuzzy=True))
    
    for date in date_list:
        date_list_str.append(date.strftime("%d-%m-%Y"))
    return date_list_str


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        dt = parse(string, fuzzy=fuzzy)
        x = dt - (datetime.datetime.now() - datetime.timedelta(days = 7))
        if x.days < 0:
            return False
        return dt
    except ValueError:
        return False




if __name__ == "__main__":
    pass