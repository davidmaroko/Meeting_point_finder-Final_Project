import json
import os

from finding_optimal_meeting_point.local_data_base import users, get_users, append_to_users, restart_users, \
    remove_from_users

offered = "OFFERED"
confirm = "CONFIRM"
ready = "READY"
not_registered = "NOT_REGISTERED"


def write_users_list_to_file(filename):
    with open(filename, 'w') as file:
        json.dump(get_users(), file)


def read_users_list_from_file(filename):
    users_list = []
    try:
        with open(filename, 'r') as file:
            users_list = json.load(file)
            print(users_list)
            for u in users_list:
                u['point'] = tuple(u['point'])
                if u['meeting_point'] is not None:
                    u['meeting_point'] = tuple(u['meeting_point'])
        return users_list
    except Exception as e:
        print("except in read_users_list_from_file, mayby file are empty")
        return get_users()


def set_users_to_offered(points, filename, meeting_point):
    print("meeting_point: ",meeting_point)
    users_copy = get_users()
    for p in points:
        for i, u in enumerate(users_copy):
            if u['point'] == p:
                users_copy[i]['status'] = offered
                users_copy[i]['meeting_point'] = meeting_point

    restart_users(users_copy)
    write_users_list_to_file(filename)


def set_user_status(email, status, filename):
    restart_users(read_users_list_from_file(filename))
    users_copy = get_users()
    for i, u in enumerate(users_copy):
        if u['email'] == email:
            users_copy[i]['status'] = status
    restart_users(users_copy)
    write_users_list_to_file(filename)


def set_user_to_ready(point, filename):
    users_copy = get_users()
    for i, u in enumerate(users_copy):
        if u['point'] == point:
            users_copy[i]['status'] = ready
    restart_users(users_copy)
    write_users_list_to_file(filename)


def check_if_there_10_confirmations(prayers, file_name):
    restart_users(read_users_list_from_file(file_name))
    count = 0
    users_copy = get_users()
    print("users_copy: ", users_copy)
    print("uses_copy len: ", len(users_copy))
    print("prayers: ", prayers)
    for p in prayers:
        for i, u in enumerate(users_copy):
            if u['point'] == p and u['status'] == confirm:
                count += 1
    print("count: ", count)
    if count >= 10:
        return True
    return False


def add_user_to_users(data, file_name):
    users_copy = read_users_list_from_file(file_name)
    print("users_copy: ", users_copy)
    restart_users(users_copy)
    for u in users_copy:
        if u['email'] == data['email']:
            if u['status'] != ready:
                return False
            u['point'] = data['point']
            u['status'] = None
            u['meeting_point'] = None
            write_users_list_to_file(file_name)
            return True
    append_to_users(data)
    write_users_list_to_file(file_name)
    return True


def get_user_status(email, filename):
    users_copy = read_users_list_from_file(filename)
    restart_users(users_copy)
    for u in users_copy:
        if u['email'] == email:
            return {"status": u['status'], 'meeting_point': u['meeting_point']}
    return {"status": 'NOT_REGISTERED'}


def delete_user(email, filename):
    users_copy = read_users_list_from_file(filename)
    restart_users(users_copy)
    user_to_delete = None
    for user in users_copy:
        if user['email'] == email:
            user_to_delete = user
    users_copy.remove(user_to_delete)
    restart_users(users_copy)
    write_users_list_to_file(filename)
    print("after delete: ", read_users_list_from_file(filename))


def set_user_status_with_meeting_point(meeting_point, status, filename):
    print(meeting_point)
    print(status)
    users_copy = read_users_list_from_file(filename)
    restart_users(users_copy)
    users_copy = get_users()
    for i, u in enumerate(users_copy):
        print (u['meeting_point'])
        if u['meeting_point'] == meeting_point:
            users_copy[i]['status'] = status
            print("got here2")
    restart_users(users_copy)
    write_users_list_to_file(filename)


def get_user_by_email(email, filename):
    users_copy = read_users_list_from_file(filename)
    restart_users(users_copy)
    for u in users_copy:
        if u['email'] == email:
            print("user: ", u)
            return u
    print("not found, users_copy: ", users_copy)
