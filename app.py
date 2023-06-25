import os
import threading
import osmnx as ox
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from flask_cors import CORS
import json
from datetime import datetime, timedelta

from finding_optimal_meeting_point import return_bbox_from_list, find_optimal_node, find_nearest_nodes, extreme_points
from finding_optimal_meeting_point.data_base import add_point_to_list, remove_points_from_dicts_list
from finding_optimal_meeting_point.local_data_base import remove_from_minianim, get_users, restart_minianim
from finding_optimal_meeting_point.minian_data_base import add_minian_to_minianim, read_minianim_list_from_file, \
    set_minian_to_done, delete_minian, write_minianim_list_to_file
from finding_optimal_meeting_point.users_data_base import set_users_to_offered, add_user_to_users, get_user_status, \
    check_if_there_10_confirmations, set_user_to_ready, set_user_status, delete_user, \
    set_user_status_with_meeting_point, get_user_by_email
from finding_optimal_meeting_point.connected_system import search_for_coverage, check_connectivity, \
    disconnect_disconnected_nodes, is_within_distance_or_rectangle

dir_path = os.path.dirname(os.path.realpath(__file__))

# path_to_users_data_base = 'C:/Users/dmaro/PycharmProjects/flaskProject/users_data.json'
path_to_users_data_base = dir_path+'/users_data.json'
path_to_dicts_data_base = dir_path+'/group_data.json'
# path_to_dicts_data_base = 'C:/Users/dmaro/PycharmProjects/flaskProject/group_data.json'
# path_to_minian_data_base = 'C:/Users/dmaro/PycharmProjects/flaskProject/minian_data.json'
path_to_minian_data_base = dir_path+'/minian_data.json'

distance = 4000  # distance from the frame that surrounds a group of people
border = 500  # how meters away from the most extreme people`s location
radius = 8000  # the redis of the circle in search coverage function
skipping = 20  # the sum of the vertex in graph will divided in this parameter
radius_for_second_search = 400  # the radius of the second search after the approximate point is found
max_minute_passed = 40  # max passed minute from the begin of the minian

offered = "OFFERED"
confirm = "CONFIRM"
ready = "READY"
reject = "REJECT"
rejected = "ARE_REJECTED"

app = Flask(__name__)
CORS(app)

response_data = {}  # Store response data per session ID


@app.route('/', methods=['GET'])
@cross_origin()
def do_get_status():
    """the user want to know what his status"""
    print("in do_get_status ,return the status")
    email = request.args.get('email')
    response_dict = get_user_status(email, path_to_users_data_base)
    if response_dict['status'] == rejected:
        set_user_status(email, None, path_to_users_data_base)
    return jsonify(response_dict)


@app.route('/confirm', methods=['POST'])
@cross_origin()
def do_post_confirm():
    """the user confirm the minian that offered"""
    print("in do_post_confirm")
    data = request.get_json()  # Assuming the request payload is in JSON format
    print(data)
    threading.Thread(target=process_confirm, args=(data,)).start()
    return jsonify({'status': 'your confirmation has received and being processed'})


@app.route('/reject', methods=['POST'])
@cross_origin()
def do_post_reject():
    """the user reject the minian that offered"""
    print("in do_post_reject")
    data = request.get_json()  # Assuming the request payload is in JSON format
    print(data)

    threading.Thread(target=process_reject, args=(data,)).start()
    return jsonify({'status': 'your reject has received and being processed'})


@app.route('/rejectArea', methods=['POST'])
@cross_origin()
def do_post_reject_area():
    """the user reject the minian that ready in the area"""
    print("in do_post_reject_area")
    data = request.get_json()  # Assuming the request payload is in JSON format
    point = data.get('point', 'default')
    email = data.get('email', '')
    point = tuple(map(float, point.split(',')))
    print(data)
    print("point: ",point, " email: ",email , " number: ",data.get('number', 1))
    delete_user(email, path_to_users_data_base)
    add_user_to_users({'point': point, 'email': email, 'status': None, 'meeting_point': None}, path_to_users_data_base)
    threading.Thread(target=process_data, args=(data, False)).start()  # False is for not search in the area
    return jsonify({'status': 'your reject has received and being processed, the system search again'})


@app.route('/', methods=['POST'])
@cross_origin()
def do_post_new_user():
    """post new point with details"""
    print("in do_post_new_user")
    data = request.get_json()  # Assuming the request payload is in JSON format
    point = data.get('point', 'default')
    email = data.get('email', '')
    point = tuple(map(float, point.split(',')))
    print(path_to_users_data_base)
    if not add_user_to_users({'point': point, 'email': email, 'status': None, 'meeting_point': None},
                             path_to_users_data_base):
        return jsonify({'status': 'you have already previous request'})
    threading.Thread(target=process_data, args=(data,)).start()
    return jsonify({'status': 'Request received and being processed'})


def process_data(data, not_reject_minian_in_area=True):
    print("in proces_data")
    point = data.get('point', 'default')
    number = data.get('number', 1)
    point = tuple(map(float, point.split(',')))
    if not_reject_minian_in_area and check_minian_in_area(point, number):
        return

    print("point: ", point, "num of people: ", number)
    coverage = False
    for p in range(int(number)):
        if add_point_to_list(point, distance, path_to_dicts_data_base):
            coverage = True
    if coverage is False:
        print("not add dic with 10 or more")
        return
    points_for_graph = search_for_coverage(radius)
    print(type(points_for_graph))
    if len(points_for_graph) == 0:
        print("not found coverage")
        return
    G = return_bbox_from_list(points_for_graph, border)
    secondG = check_connectivity(G, points_for_graph, 500)
    if secondG is None:
        print("found 10 people but they can`t connect")
        return
    nn = find_nearest_nodes(G, points_for_graph)

    G = disconnect_disconnected_nodes(G, nn[0])
    secondG = disconnect_disconnected_nodes(secondG, nn[0])
    meeting_point = find_optimal_node(G, secondG, points_for_graph, skipping, radius_for_second_search)
    meeting_location = (G.nodes[meeting_point]['y'], G.nodes[meeting_point]['x'])
    create_minian(points_for_graph, meeting_location)
    plot_graph_with_points(G, points_for_graph, meeting_point, nn)


def create_minian(points_for_graph, meeting_point):
    ne, sw = extreme_points(points_for_graph)
    current_timestamp = datetime.now()
    time_json = json.dumps(current_timestamp, default=str)
    remove_points_from_dicts_list(points_for_graph, path_to_dicts_data_base)
    new_minian = {'meeting_point': meeting_point,
                  'points': points_for_graph,
                  'northeastern': ne,
                  'southwest': sw,
                  'first_time_stamp': time_json,
                  'second_time_stamp': None}
    add_minian_to_minianim(new_minian, path_to_minian_data_base)
    set_users_to_offered(points_for_graph, path_to_users_data_base, meeting_point)
    # timestamp = datetime.fromisoformat(timestamp_str)


def plot_graph_with_points(G, points_for_graph, meeting_point, nn):
    node_colors = ['r' if node == meeting_point else 'w' if node not in nn else 'b' for node in G.nodes()]
    node_size = [70 if node == meeting_point else 10 if node not in nn else 40 for node in G.nodes()]
    fig, ax = ox.plot_graph(G, node_color=node_colors, node_edgecolor='k', node_size=node_size, node_zorder=3,
                            edge_linewidth=1)


def check_minian_in_area(point, number):
    minianim_copy = read_minianim_list_from_file(path_to_minian_data_base)
    if len(minianim_copy) > 0:
        for i, m in enumerate(minianim_copy):
            if is_within_distance_or_rectangle(point, minianim_copy[i]['northeastern'], minianim_copy[i]['southwest'],
                                               distance):
                if minianim_copy[i]['second_time_stamp'] is not None:
                    if check_minutes_passed(minianim_copy[i]['second_time_stamp'], max_minute_passed) is False:
                        set_users_to_offered([point], path_to_users_data_base, minianim_copy[i]['meeting_point'])
                        set_user_to_ready(point, path_to_users_data_base)
                        return True
                else:
                    if check_minutes_passed(minianim_copy[i]['first_time_stamp'], max_minute_passed) is False:
                        print("number: ", number)
                        print("minian before adding: ", minianim_copy[i]['points'])
                        for n in range(int(number)):
                            print("adding ", point, " to minian")
                            minianim_copy[i]['points'].append(point)
                        print("minian after adding: ", minianim_copy[i]['points'])
                        restart_minianim(minianim_copy)
                        write_minianim_list_to_file(path_to_minian_data_base)
                        set_users_to_offered([point], path_to_users_data_base, minianim_copy[i]['meeting_point'])
                        return True
    return False


def process_confirm(data):
    email = data.get('email', '')
    meeting_point = data.get('meeting_point', '')
    meeting_point = tuple(meeting_point)
    set_user_status(email, confirm, path_to_users_data_base)
    minian_list = read_minianim_list_from_file(path_to_minian_data_base)
    minian_prayers = []
    for minian in minian_list:
        if minian['meeting_point'] == meeting_point:
            print("same")
            for p in minian['points']:
                minian_prayers.append(p)
    print("minian prayers len: ", len(minian_prayers))
    if check_if_there_10_confirmations(minian_prayers, path_to_users_data_base):
        print("exist 10 people that confirmed")
        for prayer in minian_prayers:
            set_user_to_ready(prayer, path_to_users_data_base)
        set_minian_to_done(meeting_point, path_to_minian_data_base)
    else:
        print("not all the minian prayers are confirmed yet")


def process_reject(data):
    print("in proces_reject")
    email = data.get('email', '')
    user = get_user_by_email(email, path_to_users_data_base)
    point = user['point']
    meeting_point = data.get('meeting_point', '')
    meeting_point = tuple(meeting_point)
    print("email: ", email)
    print("point:", point)
    print("meeting_point: ", meeting_point)
    delete_user(email, path_to_users_data_base)
    minian_list = read_minianim_list_from_file(path_to_minian_data_base)
    check_minian = []
    for minian in minian_list:
        if minian['meeting_point'] == meeting_point:
            check_minian = minian
    filtered_points = []
    for p in check_minian['points']:
        if p != point:
            filtered_points.append(p)
    print("count: ", len(filtered_points))
    if len(filtered_points) < 10:
        delete_minian(check_minian['meeting_point'], path_to_minian_data_base)
        for p in filtered_points:
            add_point_to_list(p, distance, path_to_dicts_data_base)
            print("added to list")
        set_user_status_with_meeting_point(meeting_point, rejected, path_to_users_data_base)

        print("got here")


def check_minutes_passed(timestamp, x):
    print("in check minute")
    # Remove the extra quotes from the timestamp string
    timestamp = timestamp.strip('"')
    # Convert the timestamp string to a datetime object
    timestamp_datetime = datetime.fromisoformat(timestamp)
    # Calculate the current time
    current_time = datetime.now()
    # Calculate the time difference between the current time and the timestamp
    time_difference = current_time - timestamp_datetime
    # Convert X minutes to a timedelta object
    X_minutes = timedelta(minutes=x)
    # Check if X minutes have passed since the timestamp
    if time_difference >= X_minutes:
        print("passed")
        return True
    else:
        print("not passed already")
        return False


def process_coordinates(point):
    print("Original point:", point)
    # Remove unnecessary characters from the string
    cleaned_point = point.replace(',', '').strip()
    print("Cleaned point:", cleaned_point)
    # Split the cleaned string into individual coordinate values
    coordinates = cleaned_point.split()
    print("Coordinates:", coordinates)
    # Convert each coordinate value to a float
    float_coordinates = [float(coord) for coord in coordinates]
    print("Float coordinates:", float_coordinates)

    # Create a tuple from the float coordinates
    point_tuple = tuple(float_coordinates)
    print("Final point tuple:", point_tuple)

    return point_tuple


if __name__ == '__main__':
    app.run()
