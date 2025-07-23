import json
import os

def fetch_data():
    data = []
    base_path = os.path.join(os.path.dirname(__file__), 'data')

    for filename in os.listdir(base_path):
        if filename.endswith('.json'):
            filepath = os.path.join(base_path, filename)
            with open(filepath, 'r') as f:
                try:
                    service_data = json.load(f)
                    data.extend(service_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {filename}: {e}")
    return data
