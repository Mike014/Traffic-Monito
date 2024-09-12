document.addEventListener('DOMContentLoaded', function () {
    var mapElement = document.getElementById('map');
    if (!mapElement) {
        console.error('Elemento con ID "map" non trovato.');
        return;
    }

    var map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var startMarker, endMarker;

    map.on('click', function (e) {
        var startCoordinatesElement = document.getElementById('start-coordinates');
        var endCoordinatesElement = document.getElementById('end-coordinates');
        if (!startCoordinatesElement || !endCoordinatesElement) {
            console.error('Elementi con ID "start-coordinates" o "end-coordinates" non trovati.');
            return;
        }

        if (!startMarker) {
            startMarker = L.marker(e.latlng).addTo(map).bindPopup("Start Point").openPopup();
            startCoordinatesElement.value = JSON.stringify(e.latlng);
        } else if (!endMarker) {
            endMarker = L.marker(e.latlng).addTo(map).bindPopup("End Point").openPopup();
            endCoordinatesElement.value = JSON.stringify(e.latlng);
        }
    });

    var calculatePathButton = document.getElementById('calculate-path');
    if (!calculatePathButton) {
        console.error('Elemento con ID "calculate-path" non trovato.');
        return;
    }

    calculatePathButton.addEventListener('click', function () {
        var startCoordinatesElement = document.getElementById('start-coordinates');
        var endCoordinatesElement = document.getElementById('end-coordinates');
        if (!startCoordinatesElement || !endCoordinatesElement) {
            console.error('Elementi con ID "start-coordinates" o "end-coordinates" non trovati.');
            return;
        }

        var startCoordinates = JSON.parse(startCoordinatesElement.value);
        var endCoordinates = JSON.parse(endCoordinatesElement.value);
        calculateShortestPath(startCoordinates, endCoordinates);
    });

    function calculateShortestPath(start, end) {
        var osrmUrl = `https://router.project-osrm.org/route/v1/driving/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson`;

        fetch(osrmUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error in server response');
                }
                return response.json();
            })
            .then(data => {
                if (!data.routes || data.routes.length === 0) {
                    console.error('Error: The returned route is empty or invalid.');
                    return;
                }

                var route = data.routes[0].geometry.coordinates;

                // Clear the map of previous routes
                map.eachLayer(function (layer) {
                    if (layer instanceof L.Polyline) {
                        map.removeLayer(layer);
                    }
                });

                // Add the shortest route to the map
                var polyline = L.polyline(route.map(coord => [coord[1], coord[0]]), { color: 'blue' }).addTo(map);
                map.fitBounds(polyline.getBounds());

                // Add markers for the start and end points
                L.marker([route[0][1], route[0][0]]).addTo(map).bindPopup("Start Point").openPopup();
                L.marker([route[route.length - 1][1], route[route.length - 1][0]]).addTo(map).bindPopup("End Point").openPopup();

                // Request traffic prediction
                fetch('/predict_traffic', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        route: route
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Error in server response');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Traffic prediction response:', data); // Log the response for debugging
                        if (!data || !data.traffic_description) {
                            console.error('Error: The traffic prediction is empty or invalid.');
                            return;
                        }

                        // Display traffic information
                        var trafficInfoElement = document.getElementById('traffic-info');
                        if (trafficInfoElement) {
                            var trafficInfo = "Traffic prediction: " + data.traffic_description;
                            trafficInfoElement.innerText = trafficInfo;
                        } else {
                            console.error('Elemento con ID "traffic-info" non trovato.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred while predicting traffic. Please try again.');
                    });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while calculating the route. Please try again.');
            });
    }
});





















