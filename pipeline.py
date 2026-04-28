# pipeline.py
import schedule
import time
import logging
from datetime import datetime
from config import LOG_PATH

from extract   import fetch_weather
from transform import clean_data
from load      import save_to_db
from analyze   import run_all

# --- logging setup ---
# writes to both your terminal AND a log file simultaneously
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)


def run_pipeline():
    logging.info("========== Pipeline triggered ==========")
    start = datetime.now()

    try:
        # Stage 1 — Extract
        logging.info("Step 1/3: Extracting...")
        raw = fetch_weather()

        # Stage 2 — Transform
        logging.info("Step 2/3: Transforming...")
        current, hourly = clean_data(raw)

        # Stage 3 — Load
        logging.info("Step 3/3: Loading...")
        save_to_db(current, hourly)

        elapsed = (datetime.now() - start).seconds
        logging.info(f"Pipeline complete in {elapsed}s")

        # print analysis report after every successful run
        run_all()

    except Exception as e:
        logging.error(f"Pipeline FAILED: {e}")


# --- scheduler setup ---
schedule.every().day.at("06:00").do(run_pipeline)
schedule.every().day.at("12:00").do(run_pipeline)
schedule.every().day.at("18:00").do(run_pipeline)

logging.info("Scheduler started — running pipeline once immediately...")

# run once immediately so you see it work right away
run_pipeline()

logging.info("Scheduler now waiting for next trigger (6am, 12pm, 6pm daily)...")

# keep the program alive, checking every 60 seconds
while True:
    schedule.run_pending()
    time.sleep(60)