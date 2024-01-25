import os
import pandas as pd
import json

POLLUTANT_ID_CONVERSION = {'8':'NO2', '5': 'PM10', '6001': 'PM25',
                            '1': 'SO2', '7': 'O3'}

LEFT_UP = {"LAT": 46.47713492720725, "LONG":10.72030291968136}
LEFT_BOTTOM = {"LAT":45.922571254640175,"LONG": 10.56311627043269}
RIGHT_UP = {"LAT": 46.4704290320345, "LONG":11.824782562358994}
RIGHT_BOTTOM = {"LAT":45.83735326997908, "LONG":11.216901449777854}

STATION_CODES = set()
for file in os.listdir("csv_conversion/"):
    if file.endswith(".csv"):
        #print(file)
        code = file.split("_")[0]
        STATION_CODES.add(code)



def get_history_stations():


    #get unique station codes


    print(STATION_CODES)
    print(len(STATION_CODES))

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
            for code in STATION_CODES:
                #print(code)
                for value in column_values_long_names:
                        if code in value:
                            #print("found")
                            row_value = daily_file.loc[daily_file['SAMPLINGPOINT_LOCALID']== value]
                            LATITUDE = row_value['LATITUDE'].values[0]
                            LONGITUDE = row_value['LONGITUDE'].values[0]
                            if LATITUDE < LEFT_BOTTOM['LAT'] or LATITUDE > LEFT_UP['LAT']:
                                continue
                            if LONGITUDE < LEFT_UP['LONG'] or LONGITUDE > RIGHT_UP['LONG']:
                                continue
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

    #save station name and station municipality
    print(len(name_station_mappings_location))
    with open('history_data_stations_location_filtered.json', 'w') as file:
        json.dump(name_station_mappings_location, file)

    #print("not found:", len(not_found))
    #print("found length:", len(name_mappings_LAT))

def merge_filter_data():
    station_codes_found_pollutants = []
    NO2_data = pd.DataFrame()
    PM10_data = pd.DataFrame()
    PM25_data = pd.DataFrame()
    SO2_data = pd.DataFrame()
    O3_data = pd.DataFrame()
    # ['38', '5', '5015', '8', '7', '8', '6001', '7', '9', '5', '9']
    # ['38', '5', '5015', '8', '7', '8', '6001', '7', '9', '5', '9']
    dataframe_pollutant_code = {"8": NO2_data, "5": PM10_data, "6001": PM25_data, "1": SO2_data, "7": O3_data}
    filtered_stations_data = {}
    with open('history_data_stations_location_filtered.json', 'r') as file: # 'daily_pollution_stations_converted_filtered.json'
        filtered_stations_data = json.load(file)
    pollutant_codes = list(POLLUTANT_ID_CONVERSION.keys())
    for file in os.listdir("csv_conversion/"):
        if file.endswith(".csv"):
            pollutant_code = file.split("_")[1].rstrip(".csv")
            station_code = file.split("_")[0]
            if station_code not in list(filtered_stations_data.keys()):
                continue
            print(pollutant_code)
            print(pollutant_codes)
            station_codes_found_pollutants.append(pollutant_code)
            if pollutant_code not in pollutant_codes:
                continue
            print("Found match")
            pollutant_data = pd.read_csv("csv_conversion/" + file)
            dataframe_pollutant_code[pollutant_code] = pd.concat([dataframe_pollutant_code[pollutant_code], pollutant_data], ignore_index=True)
    # create folder if doesnt exist
    if not os.path.exists("historical_data"):
        os.makedirs("historical_data")
    for pollutant_code in dataframe_pollutant_code:
        dataframe_pollutant_code[pollutant_code].to_csv(f"historical_data/historical_{POLLUTANT_ID_CONVERSION[pollutant_code]}.csv", index=False)
    print(station_codes_found_pollutants)
    




if __name__ == "__main__":
    #get_history_stations()
    merge_filter_data()