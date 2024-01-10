# climateservAccess

[![Python: 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About
A python package to access data through [ClimateSERV API](https://climateserv.servirglobal.net/help). Built as a more complete, customized version of the existing [climateserv](https://pypi.org/project/climateserv/) library by SERVIR.
 
## Docs
Guide for usage

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
