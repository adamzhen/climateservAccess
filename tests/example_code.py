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