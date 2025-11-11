from .mt_intelligence_processor import MtAnalysis
import pandas as pd
from loging.logger import setup_logger  # make sure your logger module is correctly named

logger = setup_logger("IntelligenceCreatorMT")




def new_columns(data: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.info("Starting feature engineering on data, shape=%s", data.shape)
        df_calc = data.copy()
        market_cols = ['CATEGORY', 'MT_PARTNER', 'COUNTY']
        market_totals = df_calc.groupby(market_cols).agg({
            'SALES': 'sum',
            'QTY': 'sum'
        }).reset_index()
        market_totals.columns = market_cols + ['MARKET_TOTAL_SALES', 'MARKET_TOTAL_QTY']
        df_calc = df_calc.merge(market_totals, on=market_cols, how='left')

        df_calc['value_shares'] = df_calc.apply(
            lambda row: (row['SALES'] / row['MARKET_TOTAL_SALES'] * 100) if row['MARKET_TOTAL_SALES'] > 0 else 0.0,
            axis=1
        )
        df_calc['volume_shares'] = df_calc.apply(
            lambda row: (row['QTY'] / row['MARKET_TOTAL_QTY'] * 100) if row['MARKET_TOTAL_QTY'] > 0 else 0.0,
            axis=1
        )
        df_calc['pricing_power_index'] = df_calc.apply(
            lambda row: round(row['value_shares'] / row['volume_shares'], 2) if row['volume_shares'] > 0 else None,
            axis=1
        )

        df_calc.drop(columns=['MARKET_TOTAL_SALES', 'MARKET_TOTAL_QTY'], inplace=True)
        logger.info("Feature engineering completed, resulting shape=%s", df_calc.shape)
        return df_calc

    except Exception as e:
        logger.exception("Error in new_columns: %s", e)
        raise


def intelligence_creator_mt(pwani_df: pd.DataFrame, comp_df: pd.DataFrame, brand: str,category:str, territory: str) -> dict:
    try:
        logger.info("Starting intelligence creation for brand=%s, territory=%s", brand, territory)
        pwani_df = pwani_df.copy()
        comp_df = comp_df.copy()

        pwani_df["source"] = "pwani"
        comp_df["source"] = "competitor"
        pwani_df["stores"] = pwani_df["MT_PARTNER"].astype(str) + "_" + pwani_df["BRANCH"].astype(str)

        if territory.lower() == "all":
            brand_df = pwani_df[(pwani_df["BRAND"] == brand) & (pwani_df['CATEGORY']==category)]
            if brand_df.empty:
                raise ValueError(f"Brand '{brand}' not found in data")

            if brand_df["CATEGORY"].empty:
                raise ValueError(f"No CATEGORY found for brand '{brand}'")

            internal_comp = pwani_df[(pwani_df["CATEGORY"] == category) & (pwani_df["BRAND"] != brand)]
            comp_df = comp_df[comp_df["CATEGORY"] == category]

        else:
            brand_df = pwani_df[(pwani_df["BRAND"] == brand) & (pwani_df["TERRITORY"] == territory)]
            logger.info("Filtered brand_df shape=%s", brand_df.shape)
            if brand_df.empty:
                raise ValueError(f"Brand '{brand}' not found in territory '{territory}'")

            if brand_df["CATEGORY"].empty:
                raise ValueError(f"No CATEGORY found for brand '{brand}' in territory '{territory}'")

            category = brand_df["CATEGORY"].iloc[0]
            internal_comp = pwani_df[
                (pwani_df["CATEGORY"] == category)
                & (pwani_df["TERRITORY"] == territory)
                & (pwani_df["BRAND"] != brand)
            ]
            comp_df = comp_df[(comp_df["CATEGORY"] == category) & (comp_df["TERRITORY"] == territory)]

        combined = pd.concat([brand_df, internal_comp, comp_df], ignore_index=True)
        combined = new_columns(combined)
        logger.info("Combined data shape after new_columns=%s", combined.shape)

        pwani_data = combined[(combined["BRAND"] == brand) & (combined["source"] == "pwani")]
        internal_comp = combined[(combined["BRAND"] != brand) & (combined["source"] == "pwani")]
        comp_data = combined[combined["source"] == "competitor"]

        analysis = MtAnalysis()
        logger.info("MtAnalysis instance created successfully")
        print(pwani_data.columns)
        print(internal_comp.columns)
        print(comp_data.columns)

        result = {
            "brand_name": brand,
            "territory": territory,
            "category": category,
            "overall_conclusion": analysis.overall_conclusion(pwani_data,internal_comp,comp_data),
            "internal_competition": analysis.internal_comp_md(internal_comp,pwani_data,comp_data),
            "external_competition": analysis.competitor_data_md(comp_data,pwani_data,internal_comp),
            "target_partner": analysis.partner_analysis_md(pwani_data),
            "internal_partner": analysis.partner_analysis_md(internal_comp),
            "external_partner": analysis.partner_analysis_md(comp_data),
            "target_sub_county": analysis.subcounty_analysis_md(pwani_data),
            "internal_sub_county": analysis.subcounty_analysis_md(internal_comp),
            "external_subcounty": analysis.subcounty_analysis_md(comp_data),
        }
        logger.info("Intelligence creation completed for brand=%s, territory=%s", brand, territory)
        return result

    except Exception as e:
        logger.exception("Failed to create intelligence for brand=%s, territory=%s: %s", brand, territory, e)
        raise