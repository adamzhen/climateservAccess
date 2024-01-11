# climateservAccess

[![Python: 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About
A python package to access data through [ClimateSERV API](https://climateserv.servirglobal.net/help). Built as a more complete, customized version of the existing [climateserv](https://pypi.org/project/climateserv/) package by SERVIR.
 
## Reference

This package was created in part because the existing [climateserv](https://pypi.org/project/climateserv/) package did not support all ClimateSERV datatypes. Thus, our package was built to be able to access all of them: 

| Datatype Number  | Datatype                          | Data Availability | Date Range |
|-----------|------------------------------------------|-------------------|------------|
| 0         | CHIRPS_Rainfall                          | Every 1 day       | 1981 - Near Present |
| 1         | eMODIS_NDVI_W_Africa                     | Every 10 days     | 2002 - September 2022 |
| 2         | eMODIS_NDVI_E_Africa                     | Every 10 days     | 2002 - September 2022 |
| 5         | eMODIS_NDVI_S_Africa                     | Every 10 days     | 2002 - September 2022 |
| 26        | NASA_IMERG_Late                          | Every 1 day       | 2000 - Near Present |
| 28        | eMODIS_NDVI_Central_Asia                 | Every 10 days     | 2002 - September 2022 |
| 29        | ESI_4WEEK                                | Every 7 days      | 2000 - Present |
| 31        | CHIRPS_GEFS_Forecast_Mean_Anom           | Every 1 day       | 1985 - Near Present |
| 32        | CHIRPS_GEFS_Forecast_Mean_Precip         | Every 1 day       | 1985 - Near Present |
| 33        | ESI_12WEEK                               | Every 7 days      | 2000 - Present |
| 37        | USDA_SMAP_Soil_Moisture_Profile          | Every 3 days      | March 2015 - August 2022 |
| 38        | USDA_SMAP_Surface_Soil_Moisture          | Every 3 days      | March 2015 - August 2022 |
| 39        | USDA_SMAP_Surface_Soil_Moisture_Anom     | Every 3 days      | March 2015 - August 2022 |
| 40        | USDA_SMAP_Sub_Surface_Soil_Moisture      | Every 3 days      | March 2015 - August 2022 |
| 41        | USDA_SMAP_Sub_Surface_Soil_Moisture_Anom | Every 3 days      | March 2015 - August 2022 |
| 90        | UCSB_CHIRP_Rainfall                      | Every 1 day       | 1981 - Near Present |
| 91        | NASA_IMERG_Early                         | Every 1 day       | 2000 - Near Present |
| 541       | NSIDC_SMAP_Sentinel_1Km                  | Every 1 day       | 2015 - Near Present |
| 542       | NSIDC_SMAP_Sentinel_1Km_15_day           | Every 15 days     | 2015 - Near Present |
| 661       | LIS_ET                                   | Every 1 day       | 2000 - Near Present |
| 662       | LIS_Baseflow                             | Every 1 day       | 2000 - Near Present |
| 663       | LIS_Runoff                               | Every 1 day       | 2000 - Near Present |
| 664       | LIS_Soil_Moisture_0_10cm                 | Every 1 day       | 2000 - Near Present |
| 665       | LIS_Soil_Moisture_10_40cm                | Every 1 day       | 2000 - Near Present |
| 666       | LIS_Soil_Moisture_40_100cm               | Every 1 day       | 2000 - Near Present |
| 667       | LIS_Soil_Moisture_100_200cm              | Every 1 day       | 2000 - Near Present |

### datatypeDict
Stores a dictionary with all datatype numbers and names *(see above)*

### getDataFrame
Accesses requested data through ClimateSERV API and returns it in a pandas dataframe
*(see Example Code)*
#### Parameters
* **data_type** (int): Datatype number
* **start_date** (str): Start date in MM/DD/YYYY format
* **end_date** (str): End date in MM/DD/YYYY format
* **operation_type** (string): 'Average', 'Min', or 'Max'
* **geometry_coords** (list): List of coordinates for polygon

### getBox
Returns a list with coordinates for a square centered at (**lon**, **lat**), with width **res**
#### Parameters
* **lat** (float): Latitude.
* **lon** (float): Longitude.
* **res** (float): Resolution.

## Example Code
This code snippet retrieves Stonehenge precipitation data from ClimateSERV (NASA_IMERG_Late), stores it in a pandas dataframe, and plots the data for the month of January 2023.

<pre>
import pandas as pd
import matplotlib.pyplot as plt
import climateservaccess as ca

# Define parameters
data_type = 26 # see ca.datatypeDict for data types
start_date = '01/01/2023' 
end_date = '01/30/2023'
operation_type = 'average' # valid options are: 'average', 'max', 'min'
lat = 51.17912455395276 # latitude of Stonehenge
lon = -1.8262705029300066 # longitude of Stonehenge
res = 0.01 # resolution in degrees
polygon = ca.getBox(lat, lon, res) # defines box of width res around lat, lon

# Get dataframe with data from ClimateSERV
df = ca.getDataFrame(data_type, start_date, end_date, operation_type, polygon)

# Select data from df and store inside data_df
data_df = pd.DataFrame(df['data'].to_list())
# Convert the date column to datetime format
data_df['date'] = pd.to_datetime(data_df['date'])

# Plot the data
plt.figure(figsize=(10,5))
plt.plot(data_df['date'], data_df['raw_value'])
plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.title('Average Daily Precipitation of Stonehenge')
plt.show()
</pre>

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.
