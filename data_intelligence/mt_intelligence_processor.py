import pandas as pd
from loging.logger import setup_logger


logger = setup_logger("MtAnalysis")


class MtAnalysis:
	def __init__(self):
		self.agg_named = {
			"total_revenue": ("SALES", lambda x: round(x.sum(), 4)),
			"total_volume": ("QTY", lambda x: round(x.sum(), 4)),
			"average_pricing_power": ("pricing_power_index", lambda x: round(x.mean(), 4)),
			"average_volume_share": ("volume_shares", lambda x: round(x.mean(), 4)),
			"average_value_share": ("value_shares", lambda x: round(x.mean(), 4)),
			"average_ws_score": ("WS", lambda x: round(x.mean(), 4)),
			"average_ta_fit": ("TA_FIT", lambda x: round(x.mean(), 4)),
			"average_z_score": ("Z_SCORE", lambda x: round(x.mean(), 4)),
			"store_coverage": ("stores", "nunique"),
		}

	def subcounty_analysis_md(self, df):
		try:
			logger.info("Starting subcounty_analysis_md")
			data = df.groupby(["COUNTY", "MT_PARTNER"]).agg(
				**self.agg_named,
				partners_present=("MT_PARTNER", lambda x: list(x.unique())),
				brand=("BRAND", "unique")
			).dropna(axis=1, how='all')
			logger.info("subcounty_analysis_md completed successfully")
			return data.to_csv()
		except Exception:
			logger.exception("Error in subcounty_analysis_md")
			raise

	def partner_analysis_md(self, df):
		try:
			logger.info("Starting partner_analysis_md")
			data = df.groupby("MT_PARTNER").agg(
				**self.agg_named,
				partners_present=("MT_PARTNER", lambda x: list(x.unique())),
				brand=("BRAND", "unique")
			).dropna(axis=1, how='all')
			logger.info("partner_analysis_md completed successfully")
			return data.to_csv()
		except Exception:
			logger.exception("Error in partner_analysis_md")
			raise

	def competitor_data_md(self, df,p_data,pi_data):
		try:
			logger.info("Starting competitor_data_md")
			df_agg = df.groupby('BRAND').agg(**self.agg_named).drop('store_coverage', axis=1, errors='ignore').dropna(axis=1, how='all')

			sort_cols = ['total_revenue', 'total_volume', 'average_pricing_power',
							'average_volume_share', 'average_value_share', 'average_z_score']

			df_sorted = df_agg.sort_values(by=sort_cols, ascending=False)

			top_n = 5  # keep top 5 brands
			top_brands = df_sorted.head(top_n)
			others = df_sorted.iloc[top_n:]

			others_agg = pd.DataFrame({
				'total_revenue': [round(others['total_revenue'].sum(), 4)],
				'total_volume': [round(others['total_volume'].sum(), 4)],
				'average_pricing_power': [round(others['average_pricing_power'].mean(), 4)],
				'average_volume_share': [round(others['average_volume_share'].mean(), 4)],
				'average_value_share': [round(others['average_value_share'].mean(), 4)],
				'average_z_score': [round(others['average_z_score'].mean(), 4)]
			}, index=['Others'])

			final_df = pd.concat([top_brands, others_agg])
			final_df = final_df.reset_index().rename(columns={"index": "BRAND"}).set_index("BRAND")
			a=final_df['total_volume'].sum()
			b=p_data['QTY'].sum()
			c=pi_data['QTY'].sum()
			final_df['market_share']=(final_df['total_volume']/(a+b+c))*100

			logger.info("competitor_data_md completed successfully")
			return final_df.to_csv()
		except Exception:
			logger.exception("Error in competitor_data_md")
			raise

	def internal_comp_md(self, df,int_comp, ext_comp):
		try:
			logger.info("Starting internal_comp_md")
			df_agg = df.groupby('BRAND').agg(**self.agg_named).drop('store_coverage', axis=1, errors='ignore').dropna(axis=1, how='all')
			brand_comp_volume = df_agg['total_volume'].sum()                # each internal competitor brand
			total_internal_volume = int_comp['QTY'].sum()                   # total internal competitors volume (raw)
			total_external_volume = ext_comp['QTY'].sum()                   # total external competitors volume (raw)

			# Denominator (full category market volume)
			market_volume = brand_comp_volume + total_internal_volume + total_external_volume
			df_agg['market_share']=df_agg['total_volume']/market_volume


			logger.info("internal_comp_md completed successfully")
			return df_agg.to_csv()
		except Exception:
			logger.exception("Error in internal_comp_md")
			raise

	def overall_conclusion(self, df, int_comp, ext_comp):
		try:
			logger.info("Starting overall_conclusion")

			# Aggregate brand data
			df_agg = df.groupby('BRAND').agg(**self.agg_named).dropna(axis=1, how='all')
			df_agg = df_agg.rename(columns={'store_coverage': 'total_no_of_stores'}, errors='ignore')

			# Total volumes
			brand_volume = df['QTY'].sum()
			internal_volume = int_comp['QTY'].sum()
			external_volume = ext_comp['QTY'].sum()

			# Market Share
			total_market_volume = brand_volume + internal_volume + external_volume
			df_agg['market_share'] = round((brand_volume / total_market_volume) * 100, 2) if total_market_volume > 0 else 0.0

			logger.info("overall_conclusion completed successfully")
			return df_agg.to_csv()

		except Exception:
			logger.exception("Error in overall_conclusion")
			raise