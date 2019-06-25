import pytest
import configparser 
from backend.utilities.basic_info.get_name import name
from backend.utilities.jsonpreprocessor import dict_from_json_file

config = configparser.ConfigParser()
config.read('config.ini')

stanford_nlp_path = config['DEFAULT']['stanford-core-nlp']
name_file_path = config['DEFAULT']['name-list']
blank_json = config['TEST']['blank_json']
written_json = config['TEST']['written_json']

class TestName(object):

    def test_both_empty_image(self):
        """
        Test for if only blank images are passed as input
        """
        assert(name({}, name_file_path, stanford_nlp_path, {})) == None
    
    def test_blank_empty_image(self):
        """
        Test for the blank empty images as input
        """
        blank_json_di = dict_from_json_file(blank_json)
        assert (name(blank_json_di, name_file_path, stanford_nlp_path, {})) != None

    def test_written_empty_blank_full(self):
        """
        Test if the blank image is good and passed image is empty
        """
        blank_json_di = dict_from_json_file(blank_json)
        assert (name({}, name_file_path, stanford_nlp_path, blank_json_di)) == None
    

