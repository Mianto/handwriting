import json
import re
from stanfordcorenlp import StanfordCoreNLP
import os


def get_ner(json_dict, core_nlp_path):
    """
    param: json_dict dict file containg jpg data
           core_nlp_path path of stanford-corenlp-full-2018-10-05
    return: nnp list 
    """
    ner_data = json_dict['textAnnotations'][0]['description']
    ner_data = ner_data.replace('\n',' ')

    nlp = StanfordCoreNLP(core_nlp_path)

    nnp = []
    for x in nlp.pos_tag(ner_data):
        if 'NNP' in x:
            nnp.append(x[0])
    
    return nnp


if __name__ == "__main__":
    pass