import json
import requests
from time import sleep

API_KEY = ''

LAT = '46.0714197'
LONG = '11.1264842'

localities = []
new_locations = []
with open('weather_stations.json', 'r') as f:
    localities = json.load(f)

for location in localities:
    if location['active'] == True:
        LAT = location['latitude']
        LONG = location['longitude']
        

        response = requests.get(f"http://api.airvisual.com/v2/nearest_city?lat={LAT}&lon={LONG}&key={API_KEY}")
        print("Original coordinates", LAT, LONG)

        print(response.status_code)
        if response.status_code == 200:
            print(response.text)
            response = json.loads(response.text)
            new_location = {
                'locality': response['data']['city'],
                'municipality': response['data']['state'],
                'latitude': response['data']['location']['coordinates'][0],
                'longitude': response['data']['location']['coordinates'][1],
                'pollution_aqius': response['data']['current']['pollution']['aqius'],
                'pollution_mainus': response['data']['current']['pollution']['mainus'],
                'pollution_aqicn': response['data']['current']['pollution']['aqicn'],
                'pollution_ts': response['data']['current']['pollution']['ts'],
                'weather_ts': response['data']['current']['weather']['ts'],
                'weather_tp': response['data']['current']['weather']['tp'],
                'weather_pr': response['data']['current']['weather']['pr'],
                'weather_hu': response['data']['current']['weather']['hu'],
                'weather_ws': response['data']['current']['weather']['ws'],
                'weather_wd': response['data']['current']['weather']['wd'],
                'weather_ic': response['data']['current']['weather']['ic'],
                'station_code': location['code'],
                'station_elevation': location['elevation'],
                'station_latitude': location['latitude'],
                'station_longitude': location['longitude'],
                'station_name': location['name'],
                'station_active': location['active'],
                'station_locality': location['locality']
            }
            new_locations.append(new_location)
            sleep(20)
        else:
            print(response.text)
            sleep(20)

with open('weather_station_pollution_loc.json', 'w') as f:
    json.dump(new_locations, f)