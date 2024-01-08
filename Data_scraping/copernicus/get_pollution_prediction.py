import pandas as pd
import json
import os
import subprocess
import random

pollutant_id_conversion = {'PM10': 'pm10', 'PM25': 'pm2p5', # our mapping vs ECMWF mapping
                           'SO2': 'so2', 'O3': 'go3', 'NO2': 'no2'}
pollutant_measure_type = {'NO2': 'ml', 'PM10': 'sfc', 'PM25': 'sfc', # our mapping vs ECMWF mapping
                           'SO2': 'ml', 'O3': 'ml'}

# file format naming axample: z_cams_c_ecmf_20240107120000_prod_fc_ml_024_go3.grid (24 steps prediction for go3 to reference date 20240107120000)
# z_cams_c_ecmf_20240108000000_prod_fc_sfc_024_pm2p5.grid

def get_pollution_data(stations_data: dict, pollutant: str, type: str, date: str ="20240108000000", prediction_steps: int = 36) -> pd.DataFrame:
    file_format = f"z_cams_c_ecmf_{date}_prod_fc_{type}_0{prediction_steps}_{pollutant}.grib"
    latitue = stations_data['LATITUDE']
    longitude = stations_data['LONGITUDE']
    command = f"grib_ls -l {latitue},{longitude},1 -j -p dataDate,dataTime,validityDate,validityTime prediction_data/{file_format}" # -j stands for json output
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    #print(result.stdout)
    data = json.loads(result.stdout)
    print("Pollutant processed", pollutant)
    print(len(data))
    #print(data)
    list_matches = data[-1]['neighbours'] #first model level
    min_item_index = 0
    min_item_distance = 2000
    for index, item in enumerate(list_matches):
        if item['distance'] < min_item_distance:
            min_item_index = index
            min_item_distance = item['distance']
    print("value before", list_matches[min_item_index]['value'])
    min_distance_pred_value = float(list_matches[min_item_index]['value'])*(10**9) # convert to ug/m3 from kg/m3
    print("min distance value", min_distance_pred_value, list_matches[min_item_index]['index'])
    print("unit", list_matches[min_item_index]['unit'])
    print("distance", list_matches[min_item_index]['distance'])
    return min_distance_pred_value

def read_pollution_stations(path_to_json: str) -> dict:
    with open(path_to_json, 'r') as f:
        data = json.load(f)
    return data

def get_prediction_data():
    stations_data = read_pollution_stations("daily_pollution_stations_converted_filtered.json")
    print("len station data", len(stations_data))
    datetime = "20240107120000"
    prediction_steps = 36 # how many hours in advance we want to predict
    for pullutant in pollutant_id_conversion:
        prediction_data = {"SAMPLINGPOINT_LOCALID":[], "DATETIME":[], "PREDICATION_STEP": [], "PROPERTY": [], "VALUE_NUMERIC": [], "UNIT": [], "STATIONCODE": [], "STATIONNAME": [], "LONGITUDE": [], "LATITUDE": [], "MUNICIPALITY": []}
        for station in stations_data:
            print(station)
            predicted_value = get_pollution_data(stations_data=stations_data[station], pollutant=pollutant_id_conversion[pullutant],type=pollutant_measure_type[pullutant])
            prediction_data["SAMPLINGPOINT_LOCALID"].append(station)
            prediction_data["DATETIME"].append(datetime)
            prediction_data["PREDICATION_STEP"].append(prediction_steps)
            prediction_data["PROPERTY"].append(pullutant)
            prediction_data["VALUE_NUMERIC"].append(predicted_value)
            prediction_data["UNIT"].append('ug/m3')
            prediction_data["STATIONCODE"].append(station)
            prediction_data["STATIONNAME"].append(stations_data[station]["STATION_NAME"])
            prediction_data["LONGITUDE"].append(stations_data[station]["LONGITUDE"])
            prediction_data["LATITUDE"].append(stations_data[station]["LATITUDE"])
            prediction_data["MUNICIPALITY"].append(stations_data[station]["MUNICIPALITY"])
        df = pd.DataFrame(prediction_data)
        # check whether folder exists
        if not os.path.exists("prediction_data"):
            os.makedirs("prediction_data")
        df.to_csv(f"prediction_data/cop_prediction_data_{pullutant}_{datetime}_{prediction_steps}.csv", index=False)
        
if __name__ =="__main__":
    get_prediction_data()