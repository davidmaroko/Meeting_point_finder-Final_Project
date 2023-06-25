
from networkx import NetworkXPointlessConcept
from osmnx._errors import EmptyOverpassResponse

import osmnx as ox

import math


def extreme_points(points):
    max_lat = -90
    min_lat = 90
    max_lng = -180
    min_lng = 180
    for point in points:
        lat, lng = point
        if lat > max_lat:
            max_lat = lat
        if lat < min_lat:
            min_lat = lat
        if lng > max_lng:
            max_lng = lng
        if lng < min_lng:
            min_lng = lng
    # a is northeastern, b is southwest
    return (max_lat, max_lng), (min_lat, min_lng)


def shift_point(point_tuple, meter):
    lat, lng = point_tuple
    dx = dy = meter
    # convert the dx from meters to degrees
    delta_lat = dx / 111000
    # convert the dy from meters to degrees
    delta_lng = dy / (111132.954 - 559.822 * math.cos(2 * lat) + 1.175 * math.cos(4 * lat))
    # add the delta_lat and delta_lng to the original lat and lng
    new_lat = lat + delta_lat
    new_lng = lng + delta_lng
    # return the new point
    # return new_lat, new_lng
    return {"latitude": new_lat, "longitude": new_lng}


def return_bbox_from_list(points, meter):
    # check the northeastern point and the southwest point
    northeastern, southwest = extreme_points(points)
    # move #meter meters from each point
    northeastern = shift_point(northeastern, meter)
    southwest = shift_point(southwest, -meter)
    north, south, east, west = northeastern['latitude'], southwest['latitude'], northeastern['longitude'], southwest[
        'longitude']
    try:
        print(north, south, east, west)
        G = ox.graph_from_bbox(north, south, east, west, network_type='drive', retain_all=True)
        if G.number_of_edges() == 0:
            return return_bbox_from_list(points, 2 * meter)
        return G
    except  NetworkXPointlessConcept:
        print("NetworkXPointlessConcept: distance is not enogh. increases..")
        return return_bbox_from_list(points, 2 * meter)
    except EmptyOverpassResponse:
        print("EmptyOverpassResponse: distance is not enogh. increases..")
        return return_bbox_from_list(points, 2 * meter)
    except ValueError:
        print("ValueError: distance is not enogh. increases..")
        return return_bbox_from_list(points, 2 * meter)
