import os
import pandas as pd
import json

daily_stations = {}
LEFT_UP = {"LAT": 46.47713492720725, "LONG":10.72030291968136}
LEFT_BOTTOM = {"LAT":45.922571254640175,"LONG": 10.56311627043269}
RIGHT_UP = {"LAT": 46.4704290320345, "LONG":11.824782562358994}
RIGHT_BOTTOM = {"LAT":45.83735326997908, "LONG":11.216901449777854}

daily_stations_df = pd.DataFrame(columns=['SAMPLINGPOINT_LOCALID', 'LATITUDE', 'LONGITUDE', 'MUNICIPALITY', 'STATIONCODE', 'STATIONNAME', 'PROPERTY'])

def daily_stations_extract():
    for file in os.listdir("converted_daily/"):
        if file.endswith(".csv"):
            daily_file = pd.read_csv("converted_daily/" + file)
            station_codes = daily_file['STATIONCODE'].values
            for code in station_codes: 
                row_value = daily_file.loc[daily_file['STATIONCODE']== code]
                LATITUDE = row_value['LATITUDE'].values[0]
                LONGITUDE = row_value['LONGITUDE'].values[0]
                MUNICIPALITY = row_value['MUNICIPALITY'].values[0]
                STATION_NAME = row_value['STATIONNAME'].values[0]
                PROPERTY = row_value['PROPERTY'].values[0]
                if LATITUDE < LEFT_BOTTOM['LAT'] or LATITUDE > LEFT_UP['LAT']:
                    continue
                if LONGITUDE < LEFT_UP['LONG'] or LONGITUDE > RIGHT_UP['LONG']:
                    continue

                daily_stations[code] = {}
                daily_stations[code]['LATITUDE'] = LATITUDE
                daily_stations[code]['LONGITUDE'] = LONGITUDE
                daily_stations[code]['MUNICIPALITY'] = MUNICIPALITY
                daily_stations[code]['STATIONCODE'] = code
                daily_stations[code]['STATION_NAME'] = STATION_NAME
                daily_stations[code]['PROPERTY'] = PROPERTY
    daily_stations_df = daily_stations_df.from_dict(daily_stations, orient='index')
    daily_stations_df.to_csv("daily_pollution_stations_filtered.csv", index=False)
    print(len(daily_stations))
    with open('daily_pollution_stations_converted_filtered.json', 'w') as f:
        json.dump(daily_stations, f)



def filter_daily_records():
    stations = None
    with open('daily_pollution_stations_converted_filtered.json', 'r') as f:
        stations = json.load(f)
    stations_codes = list(stations.keys())
    for file in os.listdir("converted_daily/"):
        if file.endswith(".csv"):
            daily_file = pd.read_csv("converted_daily/" + file)
            # now go line by line and check whether the station code is in the list of stations
            for index, row in daily_file.iterrows():
                if row['STATIONCODE'] not in stations_codes:
                    daily_file.drop(index, inplace=True)
            daily_file.to_csv(f"converted_daily/filtered_{file}", index=False)




if __name__ == "__main__":
    filter_daily_records()
                