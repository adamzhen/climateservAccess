# Custom library for accessing the ClimateSERV API
# By Adam Zheng

import requests
import json
import time
import pandas as pd

# Define dictionary of all datatypes and corresponding numbers
datatypeDict = {
    0: "CHIRPS_Rainfall",
    1: "eMODIS_NDVI_W_Africa",
    2: "eMODIS_NDVI_E_Africa",
    5: "eMODIS_NDVI_S_Africa",
    6: "CCSM_Ensemble_1_Temperature",
    7: "CCSM_Ensemble_1_Precipitation",
    8: "CCSM_Ensemble_2_Temperature",
    9: "CCSM_Ensemble_2_Precipitation",
    10: "CCSM_Ensemble_3_Temperature",
    11: "CCSM_Ensemble_3_Precipitation",
    12: "CCSM_Ensemble_4_Temperature",
    13: "CCSM_Ensemble_4_Precipitation",
    14: "CCSM_Ensemble_5_Temperature",
    15: "CCSM_Ensemble_5_Precipitation",
    16: "CCSM_Ensemble_6_Temperature",
    17: "CCSM_Ensemble_6_Precipitation",
    18: "CCSM_Ensemble_7_Temperature",
    19: "CCSM_Ensemble_7_Precipitation",
    20: "CCSM_Ensemble_8_Temperature",
    21: "CCSM_Ensemble_8_Precipitation",
    22: "CCSM_Ensemble_9_Temperature",
    23: "CCSM_Ensemble_9_Precipitation",
    24: "CCSM_Ensemble_10_Temperature",
    25: "CCSM_Ensemble_10_Precipitation",
    26: "NASA_IMERG_Late",
    28: "eMODIS_NDVI_Central_Asia",
    29: "ESI_4WEEK",
    31: "CHIRPS_GEFS_Forecast_Mean_Anom",
    32: "CHIRPS_GEFS_Forecast_Mean_Precip",
    33: "ESI_12WEEK",
    37: "USDA_SMAP_Soil_Moisture_Profile",
    38: "USDA_SMAP_Surface_Soil_Moisture",
    39: "USDA_SMAP_Surface_Soil_Moisture_Anom",
    40: "USDA_SMAP_Sub_Surface_Soil_Moisture",
    41: "USDA_SMAP_Sub_Surface_Soil_Moisture_Anom",
    42: "CFSv2_Ensemble_1_Temperature",
    43: "CFSv2_Ensemble_1_Precipitation",
    44: "CFSv2_Ensemble_2_Temperature",
    45: "CFSv2_Ensemble_2_Precipitation",
    46: "CFSv2_Ensemble_3_Temperature",
    47: "CFSv2_Ensemble_3_Precipitation",
    48: "CFSv2_Ensemble_4_Temperature",
    49: "CFSv2_Ensemble_4_Precipitation",
    50: "CFSv2_Ensemble_5_Temperature",
    51: "CFSv2_Ensemble_5_Precipitation",
    52: "CFSv2_Ensemble_6_Temperature",
    53: "CFSv2_Ensemble_6_Precipitation",
    54: "CFSv2_Ensemble_7_Temperature",
    55: "CFSv2_Ensemble_7_Precipitation",
    56: "CFSv2_Ensemble_8_Temperature",
    57: "CFSv2_Ensemble_8_Precipitation",
    58: "CFSv2_Ensemble_9_Temperature",
    59: "CFSv2_Ensemble_9_Precipitation",
    60: "CFSv2_Ensemble_10_Temperature",
    61: "CFSv2_Ensemble_10_Precipitation",
    62: "CFSv2_Ensemble_11_Temperature",
    63: "CFSv2_Ensemble_11_Precipitation",
    64: "CFSv2_Ensemble_12_Temperature",
    65: "CFSv2_Ensemble_12_Precipitation",
    66: "CFSv2_Ensemble_13_Temperature",
    67: "CFSv2_Ensemble_13_Precipitation",
    68: "CFSv2_Ensemble_14_Temperature",
    69: "CFSv2_Ensemble_14_Precipitation",
    70: "CFSv2_Ensemble_15_Temperature",
    71: "CFSv2_Ensemble_15_Precipitation",
    72: "CFSv2_Ensemble_16_Temperature",
    73: "CFSv2_Ensemble_16_Precipitation",
    74: "CFSv2_Ensemble_17_Temperature",
    75: "CFSv2_Ensemble_17_Precipitation",
    76: "CFSv2_Ensemble_18_Temperature",
    77: "CFSv2_Ensemble_18_Precipitation",
    78: "CFSv2_Ensemble_19_Temperature",
    79: "CFSv2_Ensemble_19_Precipitation",
    80: "CFSv2_Ensemble_20_Temperature",
    81: "CFSv2_Ensemble_20_Precipitation",
    82: "CFSv2_Ensemble_21_Temperature",
    83: "CFSv2_Ensemble_21_Precipitation",
    84: "CFSv2_Ensemble_22_Temperature",
    85: "CFSv2_Ensemble_22_Precipitation",
    86: "CFSv2_Ensemble_23_Temperature",
    87: "CFSv2_Ensemble_23_Precipitation",
    88: "CFSv2_Ensemble_24_Temperature",
    89: "CFSv2_Ensemble_24_Precipitation",
    90: "UCSB_CHIRP_Rainfall",
    91: "NASA_IMERG_Early",
    541: "NSIDC_SMAP_Sentinel_1Km",
    542: "NSIDC_SMAP_Sentinel_1Km_15_day",
    661: "LIS_ET",
    662: "LIS_Baseflow",
    663: "LIS_Runoff",
    664: "LIS_Soil_Moisture_0_10cm",
    665: "LIS_Soil_Moisture_10_40cm",
    666: "LIS_Soil_Moisture_40_100cm",
    667: "LIS_Soil_Moisture_100_200cm"
}
operationDict = {'average': 5, 'max': 0, 'min': 1}

# Define the API endpoints
submit_url = "https://climateserv.servirglobal.net/api/submitDataRequest/"
progress_url = "https://climateserv.servirglobal.net/api/getDataRequestProgress/"
data_url = "https://climateserv.servirglobal.net/api/getDataFromRequest/"

def get_data(request_ID): # helper function to retrieve the data
    response = requests.get(data_url, params={"id": request_ID})
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

def getBox(lat: float, lon: float, res: float) -> list:
    """
    Calculate the polygon coordinates for a square with dimensions of res x res, centered at (lon, lat)

    Parameters:
    lat (float): Latitude.
    lon (float): Longitude.
    res (float): Resolution.

    Returns:
    list: List of coordinates.
    """
    half_res = res / 2
    return [[lon - half_res, lat + half_res], [lon + half_res, lat + half_res],
            [lon + half_res, lat - half_res], [lon - half_res, lat - half_res], [lon - half_res, lat + half_res]]

def getDataFrame(data_type: int, start_date: str, end_date: str, operation_type: str, geometry_coords: list) -> pd.DataFrame:
    """
    Retrieve data using ClimateSERV API.

    Parameters:
    data_type (int): Data type.
    start_date (str): Start date in MM/DD/YYYY format.
    end_date (str): End date in MM/DD/YYYY format.
    operation_type (string): Operation type.
    geometry_coords (list): List of coordinates.

    Returns:
    pandas DataFrame: DataFrame containing climateserv data.
    """

    try:
        operation_type_num = operationDict[operation_type.lower().strip()]
    except KeyError:
        print(f"Invalid operation type. Valid operations are: {list(operationDict.keys())}")
        return None

    # Define the API parameters
    params = {
        'datatype': data_type,
        'begintime': start_date,
        'endtime': end_date,
        'intervaltype': 0, # 0, 1, 2 all give the same results
        'operationtype': operation_type_num,  # see operationDict for options
        'callback': 'successCallback',
        'dateType_Category': 'default',
        'geometry': json.dumps({
            "type": "Polygon",
            "coordinates": [geometry_coords]
        })
    }

    # Send the GET request
    response = requests.get(submit_url, params=params)
    request_ID = response.text
    request_ID = request_ID[ request_ID.find('[')+2 : request_ID.find("]")-1 ]

    print(f"REQUEST SUBMITTED: {datatypeDict[data_type]} [{data_type}], {start_date} to {end_date}, {operation_type}")
    # print(f"ID: {request_ID}")

    # Progress bar
    bar_length = 20
    progress_bar = f"[{bar_length * '-'}] 0%"
    print(progress_bar, end="\r")

    # Check the progress in a loop
    while True:
        response = requests.get(progress_url, params={"id": request_ID})
        try:
            progress = float(response.text[1:len(response.text)-1])
        except:
            progress = -1

        if progress >= 100: # Once complete
            break
        if progress == -1:
            print("Request failed. Error encountered.")
            return None
        
        # Update the progress bar
        nbars = int(progress/100*bar_length)
        progress_bar = f"[{nbars * '#'}{(bar_length-nbars) * '-'}] {progress:.0f}%"
        print(progress_bar, end="\r")

        time.sleep(0.1)  # Wait before checking again

    # Once complete, retrieve the data
    data = get_data(request_ID)
    print(">", end=" ")
    clear_bar = bar_length * " " # Added spaces to overwrite the progress bar
    if data is None:
        print("No data found." + clear_bar) 
        return None
    else:
        df = pd.DataFrame(data)
        if df.empty:
            print("No data found." + clear_bar)
            return None
        else:
            print("Data retrieved successfully." + clear_bar)
            return df
    
def getCSV(data_type: int, start_date: str, end_date: str, operation_type: str, geometry_coords: list, filename: str) -> None:
    """
    Retrieve data using ClimateSERV API and save as CSV.

    Parameters:
    data_type (int): Data type.
    start_date (str): Start date in MM/DD/YYYY format.
    end_date (str): End date in MM/DD/YYYY format.
    operation_type (string): Operation type.
    geometry_coords (list): List of coordinates.
    filename (str): Name of the CSV file to be saved.
    """

    # Retrieve the data
    df = getDataFrame(data_type, start_date, end_date, operation_type, geometry_coords)

    if df is not None: # If data is found, save as CSV (if not, getDataFrame will have printed an error message)
        print(">", end=" ")
        
        temp_data = pd.DataFrame(df['data'].to_list())

        # Keep only the date, raw_value, NaN columns    
        temp_data = temp_data[['date', 'raw_value']]
        # Rename raw_value to datatype
        temp_data.rename(columns={'raw_value': f"{datatypeDict[data_type]}"}, inplace=True)
        # Convert date to datetime and rename to Date
        temp_data['date'] = pd.to_datetime(temp_data['date'])
        temp_data.rename(columns={'date': 'Date'}, inplace=True)

        # Save as CSV
        temp_data.to_csv(filename, index=False)
        print(f"Data saved to {filename}.")