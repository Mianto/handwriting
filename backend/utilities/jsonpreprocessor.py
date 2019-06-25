import os
import re
import json
from pathlib import Path


def dict_from_json_file(filename):
    """
    :param string filepath: path to the json file
    :return dict: A dictionary of the files
    """
    filepath = Path(filename)
    
    if filepath.is_file():
        with open(filename, 'r') as fp:
            json_str = json.load(fp)
    else:
        return "Invalid filename or path"
        
    json_dict = eval(json_str)
    
    return json_dict


def dict_from_json(json_file):
    """
    :param json json_file: json_file from vision_api
    :return dict: a dictionary
    """
    try:
        return eval(json_file)
    except Exception as e:
        print("Exception: " + str(e))
        return None


def start_and_end_page_value(json_dict):
    """ Return the start value of the page
    :param dict json_dict: full response of the vision api in dict
    :return (int, int): start value of the page 
    :return (int, int): end value of the page
    """
    assert(type(json_dict) == dict)
    
    li1=json_dict['textAnnotations'][0]['boundingPoly']['vertices']
    li2=json_dict['textAnnotations'][1]['boundingPoly']['vertices']
    
    mi = 99999
    ma_x = -99999
    ma_y = -99999
    for i in li1:
        for j in li2:
            if mi > abs((i['x'] - j['x']) - (i['y'] - j['y'])):
                mi =  abs((i['x'] - j['x']) - (i['y'] - j['y']))
                start_x = i['x']
                start_y = i['y']
                
            if ma_x < abs((i['x'] - j['x'])) and ma_y < abs((i['y'] - j['y'])):
                ma_x = abs(i['x'] - j['x']) 
                ma_y = abs(i['y'] - j['y'])
                end_x = i['x']
                end_y = i['y']
                
    return (start_x, start_y), (end_x, end_y)


def percentage_value_of_box(box_coordinates, start, end):
    """Find the percentage of the box in according to the page
    :param list box_coordinates: boundingPoly value of the box
    :param (int, int) start: starting point of the page
    :param (int, int) end: ending point of the page
    :return float: percentage according to page
    """
    assert(type(box_coordinates) == list)
    
    start_x, start_y = start
    end_x, end_y = end
    
    average_x = 0
    average_y = 0
    for vertices in box_coordinates:
        assert(type(vertices) == type({}))
        if 'x' in vertices and 'y' in vertices:
            average_x += vertices['x']
            average_y += vertices['y']
    average_x /= len(box_coordinates)
    average_y /= len(box_coordinates)

    return (average_x - start_x)/(end_x - start_x), (average_y - start_y)/(end_y - start_y)


def box_within_percentage(json_dict, percent=0.4):
    """
    :param dict json_dict: full response of the vision api in dict
    :param float percent: percentage of page
    :return: bounding box of the page within the percent
    """
    bounding_boxes = []
    start_page, end_page = start_and_end_page_value(json_dict)
    
    for i in range(1, len(json_dict['textAnnotations']) - 2):
        boundingBox = json_dict['textAnnotations'][i]['boundingPoly']['vertices']
        if percentage_value_of_box(boundingBox, start_page, end_page)[1] < percent:
            bounding_boxes.append(json_dict['textAnnotations'][i])
            
    return bounding_boxes


def get_text_from_bounding_box(bounding_boxes):
    """
    :params list bounding_boxes: list of bounding boxes
    :return string: concatenated string
    """
    concat_string = ""
    for bounding_box in bounding_boxes:
        concat_string += bounding_box['description'] + ' '
    return concat_string


def get_adjacent_box(json_dict, box_coordinates, page_percentage=0.05, direction="y"):
    """Returns adjacent box to right and bottom
    :param dict json_dict: full response of the vision api in dict
    :param list box_coordinates: boundingPoly value of the box
    :return list of dicts: bounding box containing text
    """
    return_list = []
    start, end = start_and_end_page_value(json_dict)
    initial_box_percentage = percentage_value_of_box(box_coordinates, start, end)
    for i in range(1, len(json_dict['textAnnotations'])):
        box_i_percentage = percentage_value_of_box(json_dict['textAnnotations'][i]['boundingPoly']['vertices'], start, end)
        if direction == "x":
            if 0 < box_i_percentage[0] - initial_box_percentage[0] < page_percentage:
                return_list.append(json_dict['textAnnotations'][i])
        else:
            if 0 < box_i_percentage[0] - initial_box_percentage[0] < page_percentage:
                return_list.append(json_dict['textAnnotations'][i])
            if 0 < box_i_percentage[1] - initial_box_percentage[1] < page_percentage:
                return_list.append(json_dict['textAnnotations'][i])
        
    return return_list


def get_first_name_box(json_dict, first_name):
    """
    :param dict json_dict: full response of the vision api in dict
    :param string first_name: First Name of the patient
    :return list of dicts: Bounding box of the first name
    """
    for i in range(1, len(json_dict['textAnnotations'])):
        if first_name.lower() in json_dict['textAnnotations'][i]['description'].lower():
            return json_dict['textAnnotations'][i]['boundingPoly']['vertices']


if __name__ == "__main__":
    pass