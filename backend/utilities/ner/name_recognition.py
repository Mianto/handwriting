import json
import re
import spacy
import os


def get_ner(json_dict, core_nlp_path):
    """
    param: json_dict dict file containg jpg data
           core_nlp_path path of stanford-corenlp-full-2018-10-05
    return: nnp list 
    """
    try:
        ner_data = json_dict['textAnnotations'][0]['description']
        ner_data = ner_data.replace('\n',' ')

        nlp = spacy.load('en_core_web_sm')
        doc = nlp(ner_data)

        nnp = []
        for token in doc:
            if token.tag_ == "NNP":
                nnp.append(token.text)
                
        return nnp
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    pass