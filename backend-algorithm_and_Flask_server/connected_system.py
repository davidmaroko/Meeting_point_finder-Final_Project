import networkx as nx

from finding_optimal_meeting_point import find_nearest_nodes, return_bbox_from_list, extreme_points
from finding_optimal_meeting_point.local_data_base import  get_list_of_dicts
import math


def haversine_distance(point1, point2):
    lat1, lon1 = math.radians(point1[0]), math.radians(point1[1])
    lat2, lon2 = math.radians(point2[0]), math.radians(point2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371e3 * c  # Earth radius in meters

    return distance


def search_for_coverage(radius):
    list_of_dicts_copy = get_list_of_dicts()
    if list_of_dicts_copy and len(list_of_dicts_copy[-1]['points']) >= 10:
        return find_points_within_radius(list_of_dicts_copy[-1]['points'], radius)
    return []


def find_points_within_radius(points, radius):
    # height, width = calculate_rectangle_dimensions(
    #     haversine_distance(extreme_points(points)[0], extreme_points(points)[1]))
    # print("height: ", height, "width: ", width)

    # Calculate the conversion factors for latitude and longitude per meter
    center_point = points[0]  # Use the first point as the center point
    lat_per_meter = 1 / haversine_distance(center_point, (center_point[0] + 1, center_point[1]))
    lon_per_meter = 1 / (haversine_distance(center_point, (center_point[0], center_point[1] + 1)) * math.cos(
        math.radians(center_point[0])))

    # Try to find a circle that covers at least 10 points
    for center in points:
        count = 0
        for point in points:
            lat_diff = math.radians(point[0] - center[0])
            lon_diff = math.radians(point[1] - center[1])
            distance = haversine_distance(center, point)
            if distance <= radius:
                count += 1
        if count >= 10:
            # Circle found
            return [point for point in points if haversine_distance(center, point) <= radius]

    # Try to find a square that covers at least 10 points
    for center in points:
        count = 0
        for point in points:
            lat_diff = point[0] - center[0]
            lon_diff = point[1] - center[1]
            if abs(lat_diff) <= radius * lat_per_meter and abs(lon_diff) <= radius * lon_per_meter:
                count += 1
        if count >= 10:
            # Square found
            return [point for point in points if abs(point[0] - center[0]) <= radius * lat_per_meter and abs(
                point[1] - center[1]) <= radius * lon_per_meter]

    # No circle or square found
    return []


def calculate_rectangle_dimensions(diagonal_length):
    height = math.sqrt(diagonal_length ** 2 / 2)
    width = math.sqrt(diagonal_length ** 2 / 2)
    return height, width


def check_connectivity(graph, points, meters=500):
    # print(points)
    for i in range(3):
        if is_points_connected(graph, points):
            return graph
        # print("increase {i}", i+1)
        meters += 1500
        graph = return_bbox_from_list(points, meters)
    return None


def is_points_connected(graph, points):
    # print("searching for connections")
    people = find_nearest_nodes(graph, points)
    people_copy = people
    for node in people:
        for person in people_copy:
            if node != person:
                try:
                    nx.shortest_path(graph, person, node)
                    nx.shortest_path(graph, node, person)
                except Exception as e:
                    return False
                except nx.NetworkXNoPath as e:
                    return False

    # print("all the people are connect")
    return True


def is_within_distance_or_rectangle(req_point, ne_point, sw_point, distance):
    # Check if req_point is within the rectangle defined by ne_point and sw_point
    if sw_point[0] <= req_point[0] <= ne_point[0] and sw_point[1] <= req_point[1] <= ne_point[1]:
        return True

    # Calculate the distances between req_point and each of the rectangle's corners
    distances = [
        haversine_distance(req_point, ne_point),
        haversine_distance(req_point, (ne_point[0], sw_point[1])),
        haversine_distance(req_point, sw_point),
        haversine_distance(req_point, (sw_point[0], ne_point[1]))
    ]

    # Check if any of the distances are less than or equal to the given distance
    if any(d <= distance for d in distances):
        return True

    # If none of the above conditions are met, the point is not within distance or rectangle
    return False


def disconnect_disconnected_nodes(G, vertex):
    print("vertex: ",vertex)
    # Find all weakly connected components of the graph
    wcc = nx.weakly_connected_components(G)

    connected_components = set()
    for component in wcc:
        connected_components.add(frozenset(component))


    # Find the connected component containing vertex
    for component in connected_components:
        if vertex in component:
            # Extract the subgraph corresponding to the connected component
            subgraph = G.subgraph(component).copy()
            return subgraph

# def is_points_connected(graph, points):
#     print("in is_points_connected")
#     people = find_nearest_nodes(graph, points)
#     checked = []
#     connected = [people[0]]
#     not_connected_yet = people[1:]
#     find_unchecked_num = lambda connected, checked: next((num for num in connected if num not in checked), None)
#     while len(not_connected_yet) > 0 and len(connected) < 10:
#         changed = False
#         unchecked = find_unchecked_num(connected, checked)
#         checked.append(unchecked)
#         for node in not_connected_yet:
#             try:
#                 nx.shortest_path(graph, unchecked, node)
#                 connected.append(node)
#                 changed = True
#             except Exception as e:
#                 try:
#                     nx.shortest_path(graph, node, unchecked)
#                     connected.append(node)
#                     changed = True
#                 except Exception as e:
#                     continue
#
#         if changed or len(connected) >= 10 or find_unchecked_num(connected, checked) is not None : continue
#         print("method not find connections")
#         return False
#     print("method find connections")
#     return True
