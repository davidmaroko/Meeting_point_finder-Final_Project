
import json
from datetime import datetime
from finding_optimal_meeting_point.local_data_base import get_minian, restart_minianim, append_to_minianim


def write_minianim_list_to_file(filename):
    with open(filename, 'w') as file:
        json.dump(get_minian(), file)


def read_minianim_list_from_file(filename):
    minianim_list = []
    try:
        with open(filename, 'r') as file:
            minianim_list = json.load(file)
            for minian in minianim_list:
                minian['meeting_point'] = tuple(minian['meeting_point'])
                minian['northeastern'] = tuple(minian['northeastern'])
                minian['southwest'] = tuple(minian['southwest'])
                for i, p in enumerate(minian['points']):
                    minian['points'][i] = tuple(p)
        return minianim_list
    except Exception as e:
        print("except in read_minianim_list_from_file maybe file is empty")
        return get_minian()


def set_minian_to_done(meeting_point, filename):
    minian_copy = get_minian()
    for i, m in enumerate(minian_copy):
        if m['meeting_point'] == meeting_point:
            minian_copy[i]['second_time_stamp'] = datetime.now().isoformat()  # Convert datetime to ISO 8601 string format

    restart_minianim(minian_copy)
    write_minianim_list_to_file(filename)
# def set_minian_to_done(meeting_point, filename):
#     minian_copy = get_minian()
#     for i, m in enumerate(minian_copy):
#         if m['meeting_point'] == meeting_point:
#             minian_copy[i]['second_time_stamp'] = datetime.now()
#     restart_minianim(minian_copy)
#     write_minianim_list_to_file(filename)


def add_minian_to_minianim(data, file_name):
    print("in add minian: ", data)
    append_to_minianim(data)
    write_minianim_list_to_file(file_name)


def delete_minian(meeting_point, filename):
    minians_copy = read_minianim_list_from_file(filename)
    restart_minianim(minians_copy)
    user_to_delete = None
    for minian in minians_copy:
        if minian['meeting_point'] == meeting_point:
            minian_to_delete = minian
    minians_copy.remove(minian_to_delete)
    restart_minianim(minians_copy)
    write_minianim_list_to_file(filename)
    print("after delete: ", read_minianim_list_from_file(filename))
