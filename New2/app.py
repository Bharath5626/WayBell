from flask import Flask, request, render_template
import requests
from playsound import playsound
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Replace with your Google Maps API key
API_KEY = 'AIzaSyA_L0Ptgg6Oxc45SQGs0uD9BNj70pZ62-k'

def calculate_distance(coord1, coord2):
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def trigger_alarm():
    print("You are within 1 km of your destination!")
    playsound('alarm.mp3')  # Make sure to have an alarm sound file in the same directory

def track_location(current_coords, destination_coords):
    distance = calculate_distance(current_coords, destination_coords)
    print(f"Current distance: {distance:.2f} km")
    
    if distance <= 1.0:  # Trigger alarm if within 1 km of destination
        trigger_alarm()
        return True
    return False

@app.route('/')
def index():
    return render_template('map.html', api_key=API_KEY)

@app.route('/get_destination', methods=['POST'])
def get_destination():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    destination_coords = (lat, lng)
    print(f"Selected Destination: {destination_coords}")
    
    return "Destination received!"

@app.route('/track_location', methods=['POST'])
def track_location_route():
    data = request.json
    current_lat = data.get('current_lat')
    current_lng = data.get('current_lng')
    destination_lat = data.get('destination_lat')
    destination_lng = data.get('destination_lng')
    
    current_coords = (current_lat, current_lng)
    destination_coords = (destination_lat, destination_lng)
    
    if track_location(current_coords, destination_coords):
        return {"status": "alarm"}, 200
    else:
        return {"status": "tracking"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
