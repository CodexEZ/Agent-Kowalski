
import requests

def get_current_coordinates():
    try:
        response = requests.get("http://ip-api.com/json/")
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        if data and data["status"] == "success":
            latitude = data.get("lat")
            longitude = data.get("lon")
            if latitude is not None and longitude is not None:
                print(f"Latitude: {latitude}, Longitude: {longitude}")
            else:
                print("Could not retrieve latitude and longitude.")
        else:
            print(f"Error: {data.get('message', 'Unknown error from API')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")

if __name__ == "__main__":
    get_current_coordinates()
