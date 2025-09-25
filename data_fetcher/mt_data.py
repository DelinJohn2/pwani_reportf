import pandas as pd
from config import load_engine
from sqlmodel import create_engine
from loging.logger import setup_logger



# --- DB Engine ---
engine_name = load_engine()
engine = create_engine(engine_name)

# --- Logger ---
logger = setup_logger("DataReaderMt")


class DataReaderMt:

    def __init__(self):			
        self.pwani_rename_map = {
            "mt": "MT_PARTNER",
            "branch": "BRANCH",
            "market": "COUNTY",        
            "territory": "TERRITORY",     
            "brandName": "BRAND",
            "category": "CATEGORY",
            "supplier": "Manufacturer",
            "marketShare": "MARKET_SHARE",
            "whiteSpaceScore": "WS",
            "targetAudience": "TA_FIT",
            "brandZVol": "Z_SCORE",
            "cluster": "CLUSTER",
            "totalSales": "SALES",
            "totalQuantity": "QTY",
            "price": "PRICE",
            "competitorStrength": "COMPETITOR_STREN",
            "ERPNorm": "ERP_MT",
            "brandPriceSegment": "PRICE_SEG"
        }

        self.competitor_rename_map = {
            "territory": "TERRITORY",      
            "mt": "MT_PARTNER",
            "branch": "BRANCH",
            "market": "COUNTY",         
            "brandName": "BRAND",
            "category": "CATEGORY",
            "supplier": "Manufacturer",
            "marketShare": "MARKET_SHARE",
            "brandZVol": "Z_SCORE",
            "totalSales": "SALES",
            "totalQuantity": "QTY",
            "price": "PRICE"
        }

    def read_mt_pwani_data(self):
        query = "SELECT * FROM pwani_marketing.mt_pwani_data_cleaned"
        try:
            logger.info("Fetching MT Pwani data...")
            data = pd.read_sql_query(query, engine)
            data = data.rename(columns=self.pwani_rename_map)
            logger.info("Fetched %d rows from mt_pwani_data_cleaned", len(data))
            return data
        except Exception:
            logger.exception("Error reading MT Pwani data")
            raise

    def read_mt_competitor_data(self):
        query = "SELECT * FROM pwani_marketing.mt_competitor_data_cleaned"
        try:
            logger.info("Fetching MT Competitor data...")
            df = pd.read_sql_query(query, engine)
            df = df.rename(columns=self.competitor_rename_map)
            logger.info("Fetched %d rows from mt_competitor_data_cleaned", len(df))
            return df
        except Exception:
            logger.exception("Error reading MT Competitor data")
            raise
