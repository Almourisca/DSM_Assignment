import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"

# --- 1. GET COIMBRA DATA ---
params_coimbra = {
    "latitude": 40.2069,
    "longitude": -8.42,
    "start_date": "2025-01-01",
    "end_date": "2025-03-31",
    "hourly": ["wind_speed_10m"],
}
responses_coimbra = openmeteo.weather_api(url, params=params_coimbra)
resp_c = responses_coimbra[0]
hourly_c = resp_c.Hourly()
hourly_dataframe_COIMBRA = pd.DataFrame({
    "wind_speed_10m": hourly_c.Variables(0).ValuesAsNumpy()
})

# --- 2. GET ÉVORA DATA ---
params_evora = {
    "latitude": 38.5659,
    "longitude": -7.904,
    "start_date": "2025-01-01",
    "end_date": "2025-03-31",
    "hourly": ["wind_speed_10m"],
}
responses_evora = openmeteo.weather_api(url, params=params_evora)
resp_e = responses_evora[0]
hourly_e = resp_e.Hourly()
hourly_dataframe_EVORA = pd.DataFrame({
    "wind_speed_10m": hourly_e.Variables(0).ValuesAsNumpy()
})

# --- 3. COMBINE AND CALCULATE Q0.80 ---
combined_wind_speed = pd.concat([
    hourly_dataframe_COIMBRA['wind_speed_10m'],
    hourly_dataframe_EVORA['wind_speed_10m']
])

threshold_WS = combined_wind_speed.quantile(0.80)



print(f"\nCombined Wind Speed Q0.80 (80th percentile): {threshold_WS:.2f}")
