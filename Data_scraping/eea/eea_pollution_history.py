import os
import pandas as pd
import json

pollutant_id_conversion = {'NO2': '8', 'PM10': '5', 'PM25': '6001',
                           'SO2': '1', 'O3': '7'}

#get unique station codes
station_codes = set()
for file in os.listdir("csv_conversion/"):
    if file.endswith(".csv"):
        print(file)
        code = file.split("_")[0]
        station_codes.add(code)

print(station_codes)
print(len(station_codes))

name_mappings_LAT = {}
name_mappings_LONG = {}
name_mappings_MUN = {}
name_mappings_STAT_CODE = {}
name_mappings_STATIONNAME = {}
name_station_mappings_location = {}

not_found = set()


# loop through the files in the current folder
for file in os.listdir("converted_daily/"):
    if file.endswith(".csv"):
        daily_file = pd.read_csv("converted_daily/" + file)
        column_values_long_names = daily_file['SAMPLINGPOINT_LOCALID'].values
        for code in station_codes:
            print(code)
            for value in column_values_long_names:
                    if code in value:
                        print("found")
                        row_value = daily_file.loc[daily_file['SAMPLINGPOINT_LOCALID']== value]
                        LATITUDE = row_value['LATITUDE'].values[0]
                        LONGITUDE = row_value['LONGITUDE'].values[0]
                        MUNICIPALITY = row_value['MUNICIPALITY'].values[0]
                        STATION_CODE = row_value['STATIONCODE'].values[0]
                        STATION_NAME = row_value['STATIONNAME'].values[0]
                        if code not in name_mappings_LAT:
                            name_station_mappings_location[code] =  {}
                        """ name_mappings_LAT[code] = []
                            name_mappings_LONG[code] = []
                            name_mappings_MUN[code] = []
                            name_mappings_STAT_CODE[code] = []
                            name_mappings_STATIONNAME[code] = []
                        name_mappings_LAT[code].append(LATITUDE)
                        name_mappings_LONG[code].append(LONGITUDE)
                        name_mappings_MUN[code].append(MUNICIPALITY)
                        name_mappings_STAT_CODE[code].append(STATION_CODE)
                        name_mappings_STATIONNAME[code].append(STATION_NAME) """
                        name_station_mappings_location[code]['STATION_CODE'] = STATION_CODE
                        name_station_mappings_location[code]['STATION_NAME'] = STATION_NAME
                        name_station_mappings_location[code]['LATITUDE'] = LATITUDE
                        name_station_mappings_location[code]['LONGTITUDE'] = LONGITUDE
                        name_station_mappings_location[code]['MUNICIPALITY'] = MUNICIPALITY
                    else:
                        not_found.add(code)

#print(name_mappings_MUN)
#print(name_mappings_STAT_CODE)
#print(name_mappings_STATIONNAME)

#save station name and station municipality
print(name_station_mappings_location)
with open('history_data_stations_location.json', 'w') as file:
    json.dump(name_station_mappings_location, file)

print("not found:", len(not_found))
print("found length:", len(name_mappings_LAT))