import json
import requests

API_KEY = ''

LAT = '46.0714197'
LONG = '11.1264842'
response = requests.get(f"http://api.airvisual.com/v2/nearest_city?lat={LAT}&lon={LONG}&key={API_KEY}")

print(response.status_code)
print(response.text)