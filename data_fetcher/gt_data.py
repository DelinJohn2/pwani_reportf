import pandas as pd
from config import load_engine
from sqlmodel import create_engine

from loging.logger import setup_logger


# --- DB Engine ---
engine_name = load_engine()
engine = create_engine(engine_name)

# --- Logger ---
logger= setup_logger("DataReaderGT")


class DataReaderGT:

    def read_gt_pwani_data(self):
        query = """
            SELECT *
            FROM pwani_marketing.gt_data_pwani
            WHERE date = (SELECT MAX(date) FROM pwani_marketing.gt_data_pwani)
        """
        try:
            logger.info("Fetching GT Pwani data...")
            data = pd.read_sql(query, engine)
            logger.info("Fetched %d rows from gt_data_pwani", len(data))
            return data
        except Exception as e:
            logger.exception("Error reading GT Pwani data")
            raise

    def read_gt_competitor_data(self):
        query = """
            SELECT *
            FROM pwani_marketing.gt_competitor_data
            WHERE date = (SELECT MAX(date) FROM pwani_marketing.gt_competitor_data)
        """
        try:
            logger.info("Fetching GT Competitor data...")
            df = pd.read_sql(query, engine)
            logger.info("Fetched %d rows from gt_competitor_data", len(df))
            return df
        except Exception as e:
            logger.exception("Error reading GT Competitor data")
            raise

    def read_rtm_data(self):
        query = "SELECT * FROM pwani_marketing.rtm_data_cleaned"
        try:
            logger.info("Fetching RTM data...")
            df = pd.read_sql(query, engine)
            logger.info("Fetched %d rows from rtm_data_cleaned", len(df))
            return df
        except Exception as e:
            logger.exception("Error reading RTM data")
            raise
