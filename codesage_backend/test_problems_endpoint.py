# test_problems_endpoint.py
import requests

# URL of your running Flask server
url = "http://127.0.0.1:5000/api/v1/problems/?rating=1500"


try:
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request failed
    data = response.json()
    print("Problem fetched successfully:")
    print(data)
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")
