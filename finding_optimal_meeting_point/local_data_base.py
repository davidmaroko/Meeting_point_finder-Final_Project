list_of_dicts = []
users = []
minianim = []


def append_to_list_of_dicts(data):
    global list_of_dicts  # Declare that we want to modify the global list_of_dicts
    list_of_dicts.append(data)


def remove_from_list_of_dicts(data):
    global list_of_dicts  # Declare that we want to modify the global list_of_dicts
    list_of_dicts.remove(data)


def get_list_of_dicts():
    return list_of_dicts


def restart_list_of_dicts(data):
    global list_of_dicts  # Declare that we want to modify the global list_of_dicts
    list_of_dicts = data


def append_to_users(data):
    global users  # Declare that we want to modify the global list_of_dicts
    users.append(data)


def remove_from_users(data):
    global users  # Declare that we want to modify the global list_of_dicts
    users.remove(data)


def restart_users(data):
    global users  # Declare that we want to modify the global list_of_dicts
    users = data


def get_users():
    global users  # Declare that we want to modify the global list_of_dicts
    return users


def append_to_minianim(data):
    global minianim  # Declare that we want to modify the global list_of_dicts
    minianim.append(data)


def remove_from_minianim(data):
    global minianim  # Declare that we want to modify the global list_of_dicts
    minianim.remove(data)


def restart_minianim(data):
    global minianim  # Declare that we want to modify the global list_of_dicts
    minianim = data


def get_minian():
    return minianim
