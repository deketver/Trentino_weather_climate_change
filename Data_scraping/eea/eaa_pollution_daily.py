import requests
import json
from io import StringIO
import pandas as pd
from time import sleep
import os
import pyproj

possible_categories = {'PM25': '', 'PM10': '', 'NO2': '', 'O3': '', 'SO2': ''} # so far CO is empty

date = '20231026180000'


def get_current_data(date: str):
    for category in possible_categories:
        REQUEST_URL = f"https://discomap.eea.europa.eu/Map/UTDViewer/dataService/AllDaily?polu={category}&dt={date}" # 20231021180000, 20231017180000
        response = requests.get(REQUEST_URL)
        if response.status_code == 200:
            print(category)
            csvStringIO = StringIO(response.text)
            df = pd.read_csv(csvStringIO, sep=",")
            italian_df = df[df["STATIONCODE"].str.contains("IT")]
            print(italian_df.head())
            print(italian_df.shape)
            italian_df.to_csv(f"eea_{category}_{date[:8]}.csv", index=False)
        else:
            print(response.text)
        sleep(2)

def convert_gps_coordinates():
    transformer = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326")
    for file in os.listdir("daily/"):
        if file.endswith(".csv"):
            daily_file = pd.read_csv("daily/" + file)
            daily_file['LATITUDE'] = daily_file['LATITUDE'].apply(lambda x: transformer.transform(x, x)[0])
            daily_file['LONGITUDE'] = daily_file['LONGITUDE'].apply(lambda x: transformer.transform(x, x)[1])
            daily_file.to_csv(f"converted_{file}", index=False)


    
if __name__ == "__main__":
    convert_gps_coordinates()