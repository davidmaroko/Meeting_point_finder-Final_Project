from descartes import PolygonPatch
import geopandas as gpd
from osmnx._errors import EmptyOverpassResponse
from shapely.geometry import Point, LineString, Polygon
import networkx as nx
import osmnx as ox
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt
import math
from networkx.exception import NetworkXPointlessConcept


def find_nearest_nodes(graph, points):
    nodes_in_list = []
    for point in points:
        lng, lat = point
        nodes_in_list.append(ox.distance.nearest_nodes(graph, lat, lng))
    return nodes_in_list


def search_in_graph(msg, min_length, people, node_list, graph_for_search, skipping):
    optimal_vert = None
    index = 0
    skipping = max(1, len(node_list) // skipping)
    print("skipping each: ", skipping, " nodes")
    for vertx in node_list:
        try:
            index += 1
            if index % skipping != 0:
                continue
            pathes_length = 0
            for node in people:
                try:
                    route = nx.shortest_path(graph_for_search, node, vertx, 'length')
                    pathes_length += nx.path_weight(graph_for_search, route, 'length')
                except Exception as e:
                    try:
                        route = nx.shortest_path(graph_for_search, vertx, node, 'length')
                        pathes_length += nx.path_weight(graph_for_search, route, 'length')
                    except Exception as e:
                        raise Exception("some point are not connect ,in ",msg, " search")
                    continue
            if pathes_length <= min_length:
                print(pathes_length, " <= ", min_length, " vertx: ", vertx)
                min_length = pathes_length
                optimal_vert = vertx
        except Exception as e:
            print("not found route in ", str(e), "search ")
            continue
    if optimal_vert is None: print("optimal_vert is None")
    return optimal_vert, min_length


def build_graph_from_point(point, distance):
    try:
        G = ox.graph_from_point(point, dist=distance, network_type='drive', retain_all=True)  # dist_type='bbox'

        if G.number_of_edges() == 0:
            return build_graph_from_point(point, 2 * distance)
        return G
    except  NetworkXPointlessConcept:
        print("NetworkXPointlessConcept: distance is not enogh. increases..")
        return build_graph_from_point(point, 2 * distance)
    except EmptyOverpassResponse:
        print("ValueError: distance is not enogh. increases..")
        return build_graph_from_point(point, 2 * distance)
    except ValueError:
        print("ValueError: distance is not enogh. increases..")
        return build_graph_from_point(point, 2 * distance)


def find_optimal_node(graph, graph_for_search, points, skipping, radius):
    people = find_nearest_nodes(graph, points)
    first_node_list = list(graph.nodes())
    # print("length of first graph: ", len(first_node_list))
    min_length = 9000000
    first_optimal_vertex, min_length = search_in_graph("first", min_length, people, first_node_list, graph_for_search,
                                                       skipping=min(skipping, len(first_node_list)))
    # print("first_optimal_vertex: ", first_optimal_vertex)
    loc = (graph.nodes[first_optimal_vertex]['y'], graph.nodes[first_optimal_vertex]['x'])
    G2 = build_graph_from_point((graph.nodes[first_optimal_vertex]['y'], graph.nodes[first_optimal_vertex]['x']),
                                radius)
    second_node_list = list(G2.nodes())
    # print("length of second graph: ", len(second_node_list))
    second_optimal_vertex, min_length = search_in_graph("second", min_length, people, second_node_list,
                                                        graph_for_search, skipping=len(second_node_list))
    return second_optimal_vertex


