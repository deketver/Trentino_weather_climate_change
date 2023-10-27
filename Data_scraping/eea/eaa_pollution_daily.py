import requests
import json
from io import StringIO
import pandas as pd
from time import sleep


possible_categories = {'PM25': '', 'PM10': '', 'NO2': '', 'O3': '', 'SO2': ''} # so far CO is empty

date = '20231026180000'

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