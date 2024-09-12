# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from dijkstra import calculate_shortest_path, calculate_distance
from traffic_model import train_knn_model, predict_traffic
import pandas as pd
import logging

# Initialize the Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Example graph
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Example data for the KNN model
data = pd.DataFrame({
    'feature1': [1, 2, 3, 4],
    'feature2': [4, 3, 2, 1],
    'traffic': [100, 200, 300, 400]
})
model = train_knn_model(data)

# Return the index.html template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')
    current_conditions = data.get('current_conditions')

    if not start or not end:
        return jsonify({'error': 'Invalid input'}), 400

    try:
        path, distance, traffic_description = calculate_shortest_path(start, end, current_conditions)
        return jsonify({
            'path': path,
            'distance': distance,
            'traffic_description': traffic_description
        })
    except Exception as e:
        logging.error(f"Error calculating path: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# Test endpoint
@app.route('/test', methods=['POST'])
def test():
    try:
        data = request.json
        logging.debug(f"Received: {data}")
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        logging.error(f"Error during test: {e}")
        return jsonify({'error': str(e)}), 500

# Add endpoint for traffic prediction
@app.route('/predict_traffic', methods=['POST'])
def predict_traffic_endpoint():
    try:
        data = request.get_json()
        route = data.get('route')

        if not route:
            return jsonify({'error': 'Invalid input'}), 400

        # Log to diagnose the issue
        logging.debug(f"Received route: {route}")

        # Extract features from the route (e.g., route length)
        feature1 = len(route)  # Example: number of segments in the route
        logging.debug(f"Calculated feature1: {feature1}")

        feature2 = calculate_distance(route[0], route[-1])  # Example: total route distance
        logging.debug(f"Calculated feature2: {feature2}")

        # Predict traffic using the KNN model
        traffic_prediction = predict_traffic(model, [feature1, feature2])
        logging.debug(f"Traffic prediction: {traffic_prediction}")

        # Detailed traffic prediction description
        traffic_description = f"Predicted traffic: {traffic_prediction[0]}. "
        if traffic_prediction[0] < 100:
            traffic_description += "Light traffic."
        elif traffic_prediction[0] < 200:
            traffic_description += "Moderate traffic."
        else:
            traffic_description += "Heavy traffic."

        return jsonify({'traffic_description': traffic_description})
    except Exception as e:
        logging.error(f"Error predicting traffic: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)















