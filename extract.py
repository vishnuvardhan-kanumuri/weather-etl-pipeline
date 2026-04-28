# extract.py
import requests
import logging

# --- constants ---
CITY      = "Austin, TX"
LATITUDE  = 30.27
LONGITUDE = -97.74

API_URL = "https://api.open-meteo.com/v1/forecast"

API_PARAMS = {
    "latitude":         LATITUDE,
    "longitude":        LONGITUDE,
    "current_weather":  True,
    "hourly":           "temperature_2m,relativehumidity_2m,windspeed_10m",
    "temperature_unit": "fahrenheit",
    "windspeed_unit":   "mph",
    "timezone":         "America/Chicago",
}

# --- main function ---
def fetch_weather():
    logging.info(f"Fetching weather for {CITY}...")

    response = requests.get(
        API_URL,
        params=API_PARAMS,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()
    logging.info("API call successful.")
    return data


# --- test block ---
if __name__ == "__main__":
    import json
    logging.basicConfig(level=logging.INFO)

    raw = fetch_weather()
    print(json.dumps(raw, indent=2))