import pandas as pd
import os
import requests
from sqlalchemy import create_engine 
from datetime import datetime



URL_DB =os.getenv("URL_DB","postgresql://postgres:1234@localhost:5432/weatherdb")
#extract
city_coordinates={                     # key-value pairs in the dictionary for city_coordinates
    "Jaipur":(26.9196,75.7878),         
    "Delhi":(28.6519,77.2315),
    "Gujrat":(22.4044,88.0156)
}

API_URL="https://api.open-meteo.com/v1/forecast"   #connecting the website by API
                                                     
PARAMS_TEMPLATE={                                                #All required parameters in the dictionary Key:Values Pair
    "hourly": "temperature_2m,relative_humidity_2m,rain",
    "forecast_days": 1,
    "timezone": "auto"

}

# EXTRACTION
def fetch_weather_data(city, lat, lon):                           #taking values for the City, latitude, longitide
    params = PARAMS_TEMPLATE.copy()                               #copy parameters to not do changes in the orignal data 
    params.update({"latitude": lat, "longitude": lon})
    response= requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()


#Transform

def transform_weather_data(city, raw_data):
    hourly = raw_data['hourly']
    df = pd.DataFrame(hourly)
    df['city'] = city
    df['time'] = pd.to_datetime(df['time'])
    return df



#Load
def load_to_postgres(df,database_url):
    engine = create_engine(database_url)
    with engine.connect() as conn:
        

        df.to_sql("weather", con=conn, if_exists="append", index=False)


# Main ETL 

def run_etl():
    all_data = []
    for city,(lat, lon) in city_coordinates.items():
        print(f"Fetching weather data for {city}...")
        raw_data = fetch_weather_data(city, lat, lon)
        df = transform_weather_data(city, raw_data)
        all_data.append(df)
        print(all_data)

    final_df = pd.concat(all_data, ignore_index=True)
    print(f"Loading data into PostgreSQL...")
   
        
    load_to_postgres(final_df, URL_DB)
    print("ETL completed successfully 123.")
   
   

if __name__ == "__main__":
    run_etl()