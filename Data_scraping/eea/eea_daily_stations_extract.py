import os
import pandas as pd
import json

daily_stations = {}

for file in os.listdir("daily/"):
    if file.endswith(".csv"):
        daily_file = pd.read_csv("daily/" + file)
        station_codes = daily_file['STATIONCODE'].values
        for code in station_codes: 
            row_value = daily_file.loc[daily_file['STATIONCODE']== code]
            LATITUDE = row_value['LATITUDE'].values[0]
            LONGITUDE = row_value['LONGITUDE'].values[0]
            MUNICIPALITY = row_value['MUNICIPALITY'].values[0]
            STATION_NAME = row_value['STATIONNAME'].values[0]
            PROPERTY = row_value['PROPERTY'].values[0]

            daily_stations[code] = {}
            daily_stations[code]['LATITUDE'] = LATITUDE
            daily_stations[code]['LONGITUDE'] = LONGITUDE
            daily_stations[code]['MUNICIPALITY'] = MUNICIPALITY
            daily_stations[code]['STATION_NAME'] = STATION_NAME
            daily_stations[code]['PROPERTY'] = PROPERTY

with open('daily_pollution_stations.json', 'w') as f:
    json.dump(daily_stations, f)
                