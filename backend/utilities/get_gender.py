
def gender_printed(json_dict):
    """Get the gender of the patient
    :param dict json_dict: full response of the vision api in dict
    :return gender in case of printed gender
    """
    texts = json_dict['textAnnotations'][0]['description'].split(' ')
    i = 0
    for txt in texts:
        i += 1
        if txt.lower() == "sex" or "sex" in txt.lower():
            j = 0
            while j < 10 and len(texts[i]) == 1:
                i += 1
                j += 1
                if texts[i] == "M" or texts[i] == "F":
                    return texts[i]
    return None

if __name__ == "__main__":
    pass