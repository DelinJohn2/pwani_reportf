import pandas as pd

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

    def subcounty_analysis_md(self,df):
        data = df.groupby(["COUNTY", "MT_PARTNER"]).agg(
            **self.agg_named,
            partners_present=("MT_PARTNER", lambda x: list(x.unique())),
            brand=("BRAND", "unique")
        ).dropna(axis=1, how='all')
        return data.to_csv()
    
    def partner_analysis_md(self,df):
   
        data = df.groupby("MT_PARTNER").agg(
            **self.agg_named,
            partners_present=("MT_PARTNER", lambda x: list(x.unique())),
            brand=("BRAND", "unique")    
        ).dropna(axis=1, how='all')
        return data.to_csv()
    
    def competitor_data_md(self,df):
        df_agg = df.groupby('BRAND').agg(**self.agg_named).drop('store_coverage', axis=1).dropna(axis=1, how='all')

        sort_cols = ['total_revenue', 'total_volume', 'average_pricing_power',
                     'average_volume_share', 'average_value_share', 'average_z_score']

        df_sorted = df_agg.sort_values(by=sort_cols, ascending=False)

        top_n = 5  # for example, keep top 5 brands
        top_brands = df_sorted.head(top_n)
        others = df_sorted.iloc[top_n:]

        # Sum and mean for the "Others" group
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
        return final_df.to_csv()
    
    def internal_comp_md(self,df):
        df_agg=df.groupby('BRAND').agg(**self.agg_named).drop('store_coverage', axis=1).dropna(axis=1, how='all')
        return  df_agg.to_csv()
    
    def overall_conclusion(self,df):
        df_agg =df.groupby('BRAND').agg(**self.agg_named).dropna(axis=1, how='all').rename({'store_coverage':'total_no_of_stores'})
        return df_agg.to_csv()