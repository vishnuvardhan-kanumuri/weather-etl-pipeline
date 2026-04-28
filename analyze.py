# analyze.py
import sqlite3
import logging
from config import DB_PATH


def todays_summary():
    """
    Average, high and low temperature for today.
    """
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT
                DATE(timestamp)        AS day,
                ROUND(AVG(temp_f), 1)  AS avg_temp,
                ROUND(MAX(temp_f), 1)  AS high,
                ROUND(MIN(temp_f), 1)  AS low
            FROM hourly_weather
            WHERE DATE(timestamp) = DATE('now')
            GROUP BY day
        """).fetchone()
    return row


def hottest_hour():
    """
    The single hour today with the highest temperature.
    """
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT
                timestamp,
                temp_f
            FROM hourly_weather
            WHERE DATE(timestamp) = DATE('now')
            ORDER BY temp_f DESC
            LIMIT 1
        """).fetchone()
    return row


def humidity_peak():
    """
    The hour today with the highest humidity.
    """
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT
                timestamp,
                humidity
            FROM hourly_weather
            WHERE DATE(timestamp) = DATE('now')
            ORDER BY humidity DESC
            LIMIT 1
        """).fetchone()
    return row


def hourly_trend():
    """
    Full hourly breakdown for today — temp, humidity, wind.
    """
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT
                TIME(timestamp)  AS hour,
                temp_f,
                humidity,
                wind_mph
            FROM hourly_weather
            WHERE DATE(timestamp) = DATE('now')
            ORDER BY timestamp ASC
        """).fetchall()
    return rows


def run_all():
    print("\n========== AUSTIN TX WEATHER REPORT ==========")

    summary = todays_summary()
    if summary:
        print(f"\nToday's summary  ({summary[0]})")
        print(f"  Average temp : {summary[1]}°F")
        print(f"  High         : {summary[2]}°F")
        print(f"  Low          : {summary[3]}°F")
    else:
        print("\nNo data for today yet.")

    hot = hottest_hour()
    if hot:
        print(f"\nHottest hour   : {hot[0]}  →  {hot[1]}°F")

    humid = humidity_peak()
    if humid:
        print(f"Peak humidity  : {humid[0]}  →  {humid[1]}%")

    print("\nHourly trend (first 6 hours):")
    print(f"  {'Hour':<10} {'Temp°F':<10} {'Humidity':<12} {'Wind mph'}")
    print(f"  {'-'*44}")
    for row in hourly_trend()[:6]:
        print(f"  {row[0]:<10} {row[1]:<10} {row[2]:<12} {row[3]}")

    print("\n==============================================")


# --- test block ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_all()