# load.py
import sqlite3
import logging
from config import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS current_weather (
                timestamp  TEXT PRIMARY KEY,
                city       TEXT,
                temp_f     REAL,
                wind_mph   REAL,
                condition  TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS hourly_weather (
                timestamp  TEXT,
                city       TEXT,
                temp_f     REAL,
                humidity   INTEGER,
                wind_mph   REAL,
                PRIMARY KEY (timestamp, city)
            )
        """)
        conn.commit()
        logging.info("Database initialised.")


def save_current(record):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR IGNORE INTO current_weather
            VALUES (:timestamp, :city, :temp_f, :wind_mph, :condition)
        """, {
            **record,
            "timestamp": str(record["timestamp"])
        })
        conn.commit()
    logging.info("Current weather saved.")


def save_hourly(records):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("""
            INSERT OR IGNORE INTO hourly_weather
            VALUES (:timestamp, :city, :temp_f, :humidity, :wind_mph)
        """, [
            {**r, "timestamp": str(r["timestamp"])}
            for r in records
        ])
        conn.commit()
    logging.info(f"Saved {len(records)} hourly records.")


def save_to_db(current, hourly):
    logging.info("Loading data into database...")
    init_db()
    save_current(current)
    save_hourly(hourly)
    logging.info("Load complete.")


# --- test block ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from extract import fetch_weather
    from transform import clean_data

    raw = fetch_weather()
    current, hourly = clean_data(raw)
    save_to_db(current, hourly)

    print("\nChecking database...")

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT * FROM current_weather"
        ).fetchall()
        print("\nCurrent weather table:")
        for row in rows:
            print(row)

        rows = conn.execute(
            "SELECT * FROM hourly_weather LIMIT 3"
        ).fetchall()
        print("\nFirst 3 hourly records:")
        for row in rows:
            print(row)