# Trentino Weather and Climate Change
Repository for Knowledge Graph Engineering project focused on the creation of knowledge graph for weather and air pollution data in Trentino.

*Link to the Knowledge Graph Engineering webpage [webpage](https://unitn-knowledge-graph-engineering.github.io/KGE2023-website/)*

Project authors: **Veronika Deketova** and **Hasan Aldhahi**

## Useful links
[Official Course Website](https://unitn-knowledge-graph-engineering.github.io/KGE2023-website/) \\
[Project Repository](https://github.com/deketver/Trentino_weather_climate_change) \\
[Project Report](https://github.com/deketver/Trentino_weather_climate_change/blob/master/Documentation/KGE_2023___Trentino_Climate_Change_st.pdf) \\

## Introduction
Climate change and weather fluctuations are having significant impact on livability in many cities around the whole globe. Since industrial revolution, we observe a significant rise in the concentration of chemical substances which were not present in the atmosphere in such amounts before. The increase of air pollutant concentration can have a significant effect on human health, especially when taken in consideration more sensitive groups, such as elder people, children
and those with respiratory or cardiovascular problems. Moreover, we can refer refer to monitoring of pollutant concentration as one of the manifestation of climate change, as together with temperate rise and higher occurrence of forest fires, it is one of the consequences of climate
change. However, there are way more connections between air pollution and climate change – climate change can exacerbate air quality issues, and air quality can, in turn, contribute to climate change due to the emissions of air pollutants.
Therefore, we present here a KGE project, which allows to citizens or other tools to monitor
situation regarding the air quality data in the connection with weather forecast and other climate
situation indicators, to give a complex perception of a situation in given area. Users can then
make conclusions based on the data together with consideration of their own personal and
health interests.

## Purpose and Domain of Interest
The goal of this project is to develop a Knowledge Graph (KG) that offers thorough data regarding the weather and air quality, as climate change factor, in Trentino. The final KG is a useful tool for anyone who is looking for details on different air quality monitoring locations and pollution or weather forecasts throughout the Trentino geographical area. As well as the health impacts related to poor air quality, and the appropriate procedures to be taken to mitigate the risks. 
- Scope and Temporal Domain: 
  - Real-time measurement: Air quality and weather measures taken in real-time starting at the time of the search, providing current data.
  - 24-hour forecast: 24-hour air quality forecasts to assist users in making outdoor plans while taking future air quality conditions and weather situation into account.
  - Lastly, historical data on air quality, referring to the time from 2013 to 2024, sheds the light on Trentino's mid-range trends in air quality, and the historical data from 2013 reflects on the weather trends and temperatures in the past. 
- User Demand:
 The goal of the project is to provide a service that enables users across Trentino to access these different temporal data about different air quality observation sites and forecasts. By taking into account air quality and its historical trends as well as the forecasts with connection to the weather data, this service provided by the Knowledge graph will impact the users decision making process effectively in regards to outdoor activities, travel, and general well-being.
- Resource Structure:
Historical air pollution data gathered from 2013 form the basis of our resource, together with weather data collected since 2013. In order to create fresh historical records of air quality measurements gathered over time, this historical archive serves as a foundation. Users are always provided access to the most recent data on air quality because of real-time data feeds that continually fill the database. This historical information allows for a thorough understanding of the air quality in Trentino, making it an asset for both locals and visitors. It also allows for real-time observations and forecasts.

## Purpose Formalization
### Defined scenarios

- **Scenario 1** - The number of people with lowered immunity or suffering from breathing difficulties, or chronic health conditions is non-negligible even in the Trentino area. 

- **Scenario 2** - With growing awareness about the possible impacts of air pollution on human health increases as well number of people who are worried about spending their free time outside during unpleasant air situations. 

- **Scenario 3** - Trentino has stunning nature and many possibilities for spending time outdoors. For successful trip planning, it is useful to have information about short-term weather prediction.

- **Scenario 4** - Trentino area is very lucrative for organizing many sports events. Weather history together with air quality history can help while deciding about the ideal location and date for a sports race event.

- **Scenario 5** - Weather stability and air pollution can have a significant effect on produced agricultural products. Having long-term statistics for specific Trentino area can bring valuable information while making decisions in the agricultural field.

## Datasets
In this project, we used following datasets:
### European Environmental Agency
Up-to-date air quality data and Air Quality download service data have been used. Links for [current data](https://www.eea.europa.eu/data-and-maps/explore-interactive-maps/up-to-date-air-quality-data) and for [historical download service](https://www.eea.europa.eu/en/datahub/datahubitem-view/778ef9f5-6293-4846-badd-56a29c70880d). 
Our focus was made on following pollutants: NO2, SO2, O3, PM10 and PM2.5.

### Copernicus Atmosphere Monitoring Service
Data provided by Copernicus Atmosphere Monitoring Service in cooperation with  European Centre for Medium-range Weather Forecasts allowed to work with quality modeled data.
This service is widely accessible after granting access. Data has been downloaded via appropriate FTP server. Closer documentation and data description as available on 
[Confluence documentation](https://confluence.ecmwf.int/display/CKB/FTP+access+to+CAMS+global+data).

### Meteotrentino 
Platform focused on aspects of meteorology, snow science, and glaciology in Trentino province, [webpage](https://www.meteotrentino.it/index.html##!/home).

### Original data
Link to Google Drive folder with large size datasets: [link](https://drive.google.com/drive/folders/1tZI8BMREt87-yXYlQ85zoB6EBXQoENP5?usp=sharing)

## ER diagram
![ER diagram](/Phase_5-Data_definition/ER_diagram/ER_diagram.png)

## Formal modeling
Formal modeling was done by creating teleontology by extending our existing teleology with the reference ontologies following the language alignment. Three approaches have been used: Top-Down, Bottom-Up, and Middle-out. In all these approaches reuse the concepts from existing Knowledge resources. The main goal in iTelos process is re-usability and share-ability. Then Language alignment is used for semantic interoperability enhancement. 

### Defined data properties
Protege modeled 
![data properties](/Phase_2-Information_gathering/protege.jpeg).

### Teleontology
Final created teleontology from formal modeling phase.
![Teleontology](/Phase_4-Knowledge_definition/teleontology.jpg)

## Data Integradion

After data modeling phase in [Karma tool](https://usc-isi-i2.github.io/karma/), produced turtle files have been used as an input for Ontotext [GraphDB](https://www.ontotext.com/products/graphdb/). Created Knowledge Graph have been queried for defined competency questions.

### Final KG
[Final KG files](https://github.com/deketver/Trentino_weather_climate_change/tree/master/Phase_5-Data_definition)

Contains modified Copernicus Atmosphere Monitoring Service information 2024.

[Metadata definition](https://github.com/deketver/Trentino_weather_climate_change/blob/master/Documentation/metadata_definition.xlsx)
