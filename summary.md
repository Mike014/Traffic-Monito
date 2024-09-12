# Traffic Monitor Project Summary

The website is accessible at [https://traffic-monitor.onrender.com/](https://traffic-monitor.onrender.com/).

## index.html
The `index.html` file is the main page of the web application. It includes:
- A title "Traffic Monitor".
- An interactive map (using Leaflet) to select start and end points.
- A button to calculate the path.
- Sections to display traffic information and coordinates.

## app.py
The `app.py` file is the backend of the application, implemented with Flask. It includes:
- Initialization of the Flask app.
- Logging configuration.
- An endpoint for the main page (`/`).
- An endpoint to calculate the shortest path (`/shortest_path`).
- A test endpoint (`/test`).
- An endpoint for traffic prediction (`/predict_traffic`).

## dijkstra.py
The `dijkstra.py` file contains the implementation of Dijkstra's algorithm to calculate the shortest path. It includes:
- The `calculate_distance` function to compute the distance between two coordinates.
- The `dijkstra` function to find the shortest path in a graph.
- The `calculate_shortest_path` function that uses Dijkstra's algorithm and predicts traffic along the path.

### What is Dijkstra's Algorithm?
Dijkstra's algorithm is a graph search algorithm that finds the shortest path between two nodes in a weighted graph. It is widely used in routing and navigation systems.

## script.js
The `script.js` file handles interaction with the map and requests to the backend. It includes:
- Initialization of the Leaflet map.
- Handling click events on the map to select start and end points.
- A function to calculate the shortest path and display it on the map.
- A function to request traffic prediction from the backend.

### How We Used Maps
We used the Leaflet library to display and interact with maps. The map tiles are fetched from OpenStreetMap, and users can click on the map to set start and end points for route calculation.

## style.css
The `style.css` file contains styles for the application. It includes:
- Styles for the map.
- Styles for the coordinate and path information sections.

## traffic-monitor\__init__.py
The `__init__.py` file initializes the `traffic-monitor` module. It includes:
- Imports for the `train_knn_model`, `predict_traffic`, and `dijkstra` functions.
- Definition of the `__all__` list to specify which modules to export.

## traffic_model.py
The `traffic_model.py` file contains the machine learning model for traffic prediction. It includes:
- The `train_knn_model` function to train a K-Nearest Neighbors model.
- The `predict_traffic` function to predict traffic based on current conditions.

### What is K-Nearest Neighbors (KNN)?
K-Nearest Neighbors (KNN) is a simple, supervised machine learning algorithm used for classification and regression. It predicts the output based on the 'k' closest training examples in the feature space. In this project, we used KNN to predict traffic levels based on features such as the number of segments in the path and the total path distance.

