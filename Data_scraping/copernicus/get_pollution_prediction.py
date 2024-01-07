import pandas as pd
import json
import os
import subprocess

pollutant_id_conversion = {'NO2': 'no2', 'PM10': 'pm10', 'PM25': 'pm2p5', # our mapping vs ECMWF mapping
                           'SO2': 'so2', 'O3': 'go3'}

# file format naming axample: z_cams_c_ecmf_20240107120000_prod_fc_ml_024_go3.grid (24 steps prediction for go3 to reference date 20240107120000)

def get_pollution_data(stations_data: dict, pollutant: str, date: str ="20240107120000", prediction_steps: int = 24) -> pd.DataFrame:
    file_format = f"z_cams_c_ecmf_{date}_prod_fc_ml_0{prediction_steps}_{pollutant}.grid"
    latitue = stations_data['LATITUDE']
    longitude = stations_data['LONGTITUDE']
    command = f"grib_ls -l {latitue},{longitude},1 -j -f -p dataDate,dataTime,validityDate,validityTime {file_format}" # -j stands for json output
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
    print(result.stdout)
    data = json.loads(result.stdout)
    return data

def read_pollution_stations(path_to_json: str) -> dict:
    with open(path_to_json, 'r') as f:
        data = json.load(f)
    return data

if __name__ =="__main__":
    stations_data = read_pollution_stations("daily_pollution_stations_converted.json")
    datetime = "20240107120000"
    prediction_steps = 24 # how many hours in advance we want to predict
    for pullutant in pollutant_id_conversion:
        prediction_data = {"SAMPLINGPOINT_LOCALID":[], "DATETIME":[], "PREDICATION_STEP": [], "PROPERTY": [], "VALUE_NUMERIC": [], "UNIT": [], "STATIONCODE": [], "STATIONNAME": [], "LONGITUDE": [], "LATITUDE": [], "MUNICIPALITY": []}
        for station in stations_data:
            print(station)
            station_data = get_pollution_data(stations_data[station], pollutant_id_conversion[pullutant], datetime, prediction_steps)
            prediction_data["SAMPLINGPOINT_LOCALID"].append(station)
            prediction_data["DATETIME"].append(datetime)
            prediction_data["PREDICATION_STEP"].append(prediction_steps)
            prediction_data["PROPERTY"].append(pullutant)
            prediction_data["VALUE_NUMERIC"].append(station_data["data"][0]["value"])
            prediction_data["UNIT"].append('ug/m3')
            prediction_data["ALTITUDE"].append([stations_data[station]["ALTITUDE"]])
            prediction_data["STATIONCODE"].append(stations_data[station]["STATION_CODE"])
            prediction_data["STATIONNAME"].append(stations_data[station]["STATION_NAME"])
            prediction_data["LONGITUDE"].append(stations_data[station]["LONGTITUDE"])
            prediction_data["LATITUDE"].append(stations_data[station]["LATITUDE"])
            prediction_data["MUNICIPALITY"].append(stations_data[station]["MUNICIPALITY"])
        df = pd.DataFrame(prediction_data)
        # check whether folder exists
        if not os.path.exists("prediction_data"):
            os.makedirs("prediction_data")
        df.to_csv(f"prediction_data/prediction_data_{pullutant}_{datetime}_{prediction_steps}.csv", index=False)
        