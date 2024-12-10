import base64
import pickle
import pickletools
import json
from finding_optimal_meeting_point import extreme_points
from finding_optimal_meeting_point.connected_system import is_within_distance_or_rectangle
from finding_optimal_meeting_point.local_data_base import append_to_list_of_dicts, restart_list_of_dicts, \
    remove_from_list_of_dicts, get_list_of_dicts


def write_dictionary_list_to_file(filename):
    with open(filename, 'w') as file:
        json.dump(get_list_of_dicts(), file)


def read_dictionary_list_from_file(filename):
    dictionary_list = []
    try:
        with open(filename, 'r') as file:
            dictionary_list = json.load(file)
            for d in dictionary_list:
                for i, p in enumerate(d['points']):
                    d['points'][i] = tuple(p)
                    d['northeastern'] = tuple(d['northeastern'])
                    d['southwest'] = tuple(d['southwest'])
        return dictionary_list
    except Exception as e:
        print("except in read_dictionary_list_from_file")
        return get_list_of_dicts()


# will remove the people of the minian from the dicts list
def remove_points_from_dicts_list(points, file_name):
    print("in remove_points_from_dicts_list")
    erased = False
    data = read_dictionary_list_from_file(file_name)
    print("data: ",data)
    restart_list_of_dicts(data)
    print("get_list_of_dicts: ",get_list_of_dicts())
    list_of_dicts_copy = get_list_of_dicts()
    for d in list_of_dicts_copy:
        for p in points:
            if p in d['points']:
                d['points'].remove(p)
                erased = True
        if len(d['points']) == 0: continue
        if erased:
            d['northeastern'], d['southwest'] = extreme_points(d['points'])
            erased = False
    list_of_dicts_copy[:] = [dic for dic in list_of_dicts_copy if len(dic['points']) > 0]
    restart_list_of_dicts(list_of_dicts_copy)
    print("list_of_dicts after remove the prayers: ",get_list_of_dicts())
    write_dictionary_list_to_file(file_name)


def add_point_to_list(new_point, distance, file_name):
    restart_list_of_dicts(read_dictionary_list_from_file(file_name))
    list_of_dicts_copy = get_list_of_dicts()
    # Check if the new point is within distance of any existing point or rectangle
    matching_dicts = []
    for d in list_of_dicts_copy:
        if is_within_distance_or_rectangle(new_point, d['northeastern'], d['southwest'], distance):
            matching_dicts.append(d)

    if len(matching_dicts) == 0:
        append_to_list_of_dicts({'points': [new_point],
                              'northeastern': new_point,
                              'southwest': new_point})
        write_dictionary_list_to_file(file_name)
        return False  # no need run the coverege function

    new_dict = {'points': [],
                'northeastern': (None, None),
                'southwest': (None, None)}
    for d in matching_dicts:
        new_dict['points'] += d['points']  # connect the points
        if d in list_of_dicts_copy:
            remove_from_list_of_dicts(d)
    new_dict['points'].append(new_point)  # adding the new point
    new_dict['northeastern'], new_dict['southwest'] = extreme_points(new_dict['points'])
    append_to_list_of_dicts(new_dict)  # add the updated dictionary to the list
    write_dictionary_list_to_file(file_name)
    if len(new_dict['points']) >= 10:
        return True  # need run the coverege function
    return False  # no need run the coverege function
