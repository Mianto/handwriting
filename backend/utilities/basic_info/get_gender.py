from genderize import Genderize


def gender(first_name):
    """
    Get the gender of the patient

    :param str first_name: first_name of the patients
    :return gender in case of printed gender
    """
    try:
        li = Genderize().get([first_name])[0]
        if li['gender'] == 'male':
            return "Male"
        elif li['gender'] == 'female':
            return "Female"
        return None
    
    except Exception as e:
        print("Genderize not responding {}".format(e))
        return None

if __name__ == "__main__":
    pass