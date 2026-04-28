# transform.py
import logging
from datetime import datetime

WEATHER_CODES = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Fog",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Violent showers",
    95: "Thunderstorm",
    99: "Thunderstorm with hail",
}


def clean_current(raw, city):
    current = raw["current_weather"]
    return {
        "timestamp": datetime.fromisoformat(current["time"]),
        "city":      city,
        "temp_f":    round(current["temperature"], 1),
        "wind_mph":  round(current["windspeed"], 1),
        "condition": WEATHER_CODES.get(current["weathercode"], "Unknown"),
    }


def clean_hourly(raw, city):
    hourly   = raw["hourly"]
    times    = hourly["time"]
    temps    = hourly["temperature_2m"]
    humidity = hourly["relativehumidity_2m"]
    wind     = hourly["windspeed_10m"]

    records = []
    for i in range(len(times)):
        records.append({
            "timestamp": datetime.fromisoformat(times[i]),
            "city":      city,
            "temp_f":    round(temps[i], 1),
            "humidity":  humidity[i],
            "wind_mph":  round(wind[i], 1),
        })
    return records


def clean_data(raw, city="Austin, TX"):
    logging.info("Transforming raw API data...")
    current = clean_current(raw, city)
    hourly  = clean_hourly(raw, city)
    logging.info(f"Transformed 1 current and {len(hourly)} hourly records.")
    return current, hourly


# --- test block ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from extract import fetch_weather

    raw = fetch_weather()
    current, hourly = clean_data(raw)

    print("\n--- CURRENT ---")
    print(current)

    print("\n--- FIRST 3 HOURLY RECORDS ---")
    for record in hourly[:3]:
        print(record)