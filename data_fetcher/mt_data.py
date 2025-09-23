import pandas as pd
from config import load_engine
from sqlmodel import create_engine



engine_name=load_engine()
engine=create_engine(engine_name)


class DataReaderMt:

    def __init__(self):			
        self.pwani_rename_map = {
				"mt": "MT_PARTNER",
				"branch": "BRANCH",
				"market": "COUNTY",        # assuming 'market' = sub-county
				"territory": "TERRITORY",      # if you want both COUNTY + TERRITORY you’ll need clarification
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
        self.competitor_rename_map= {
				"territory": "TERRITORY",       # maps directly
				"mt": "MT_PARTNER",
				"branch": "BRANCH",
				"market": "COUNTY",         # assuming 'market' = sub-county
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
        data=pd.read_sql_query("SELECT * FROM pwani_marketing.mt_pwani_data_cleaned",engine)
        data=data.rename(columns=self.pwani_rename_map)
        return data

    def read_mt_competitor_data(self):
        df=pd.read_sql_query("SELECT * FROM pwani_marketing.mt_competitor_data_cleaned",engine)
        df=df.rename(columns=self.competitor_rename_map)
        return df

