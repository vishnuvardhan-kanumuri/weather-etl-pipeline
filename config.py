# config.py
CITY      = "Austin, TX"
LATITUDE  = 30.27
LONGITUDE = -97.74
TIMEZONE  = "America/Chicago"
DB_PATH   = "data/weather.db"
LOG_PATH  = "logs/pipeline.log"

API_URL = "https://api.open-meteo.com/v1/forecast"
API_PARAMS = {
    "latitude":         LATITUDE,
    "longitude":        LONGITUDE,
    "current_weather":  True,
    "hourly":           "temperature_2m,relativehumidity_2m,windspeed_10m",
    "temperature_unit": "fahrenheit",
    "windspeed_unit":   "mph",
    "timezone":         TIMEZONE,
}