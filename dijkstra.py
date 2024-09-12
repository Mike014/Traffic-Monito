# -*- coding: utf-8 -*-
import heapq
import math
import logging
from traffic_model import predict_traffic, train_knn_model
import pandas as pd

def calculate_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def dijkstra(graph, start, end, coordinates):
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path = path[::-1]
    
    if distances[end] == float('infinity'):
        logging.debug(f"No path found from {start} to {end}")
        return [], float('infinity')
    
    # Return the path with coordinates
    path_with_coordinates = [{'lat': coordinates[node][0], 'lng': coordinates[node][1]} for node in path]
    
    logging.debug(f"Calculated Path: {path_with_coordinates}")
    
    return path_with_coordinates, distances[end]

def calculate_shortest_path(start, end, current_conditions):
    # Example graph
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }

    def get_coordinates():
        return {
            'A': [51.505, -0.09],
            'B': [51.51, -0.1],
            'C': [51.52, -0.12],
            'D': [51.53, -0.13]
        }

    def get_node_for_coordinates(coordinates):
        nodes = {
            'A': [51.505, -0.09],
            'B': [51.51, -0.1],
            'C': [51.52, -0.12],
            'D': [51.53, -0.13]
        }
        closest_node = min(nodes.keys(), key=lambda node: calculate_distance(coordinates, nodes[node]))
        return closest_node

    start_node = get_node_for_coordinates(start)
    end_node = get_node_for_coordinates(end)
    path, distance = dijkstra(graph, start_node, end_node, get_coordinates())

    # Load the KNN model
    data = pd.DataFrame({
        'feature1': [1, 2, 3, 4],
        'feature2': [4, 3, 2, 1],
        'traffic': [100, 200, 300, 400]
    })
    model = train_knn_model(data)

    # Extract features from the path
    feature1 = len(path)  # Example: number of segments in the path
    feature2 = distance  # Example: total path distance

    # Predict traffic using the KNN model
    traffic_prediction = predict_traffic(model, [feature1, feature2])

    # Add log for debugging
    logging.debug(f"Traffic prediction: {traffic_prediction}")

    # Check if the traffic prediction is valid
    if not traffic_prediction or len(traffic_prediction) == 0:
        raise ValueError("The traffic prediction is empty or invalid.")

    # Detailed traffic prediction description
    traffic_description = f"The predicted traffic level is {traffic_prediction[0]}. "
    if traffic_prediction[0] < 100:
        traffic_description += "The traffic is light."
    elif traffic_prediction[0] < 200:
        traffic_description += "The traffic is moderate."
    else:
        traffic_description += "The traffic is heavy."

    return path, distance, traffic_description





