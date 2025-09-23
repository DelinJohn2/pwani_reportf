from .mt_intelligence_processor import MtAnalysis
import  pandas as pd


def new_columns(data):
    print(data.shape)
    df_calc = data.copy()
    market_cols = ['CATEGORY', 'MT_PARTNER', 'COUNTY']
    market_totals = df_calc.groupby(market_cols).agg({
        'SALES': 'sum',
        'QTY': 'sum'
    }).reset_index()
    market_totals.columns = market_cols + ['MARKET_TOTAL_SALES', 'MARKET_TOTAL_QTY']
    df_calc = df_calc.merge(market_totals, on=market_cols, how='left')

    df_calc['value_shares'] = df_calc.apply(
        lambda row: (row['SALES'] / row['MARKET_TOTAL_SALES'] * 100) 
        if row['MARKET_TOTAL_SALES'] > 0 else 0.0,
        axis=1
    )
    df_calc['volume_shares'] = df_calc.apply(
        lambda row: (row['QTY'] / row['MARKET_TOTAL_QTY'] * 100) 
        if row['MARKET_TOTAL_QTY'] > 0 else 0.0,
        axis=1
    )
    df_calc['pricing_power_index'] = df_calc.apply(
        lambda row: round(row['value_shares'] / row['volume_shares'], 2) 
        if row['volume_shares'] > 0 else None,
        axis=1
    )

    # optional: clean up helper totals
    df_calc.drop(columns=['MARKET_TOTAL_SALES','MARKET_TOTAL_QTY'], inplace=True)

    return df_calc
    
import pandas as pd

def intelligence_creator_mt(pwani_df, comp_df, brand, territory):
    pwani_df = pwani_df.copy()
    comp_df = comp_df.copy()

    # add helper cols
    pwani_df["source"] = "pwani"
    comp_df["source"] = "competitor"
    pwani_df["stores"] = pwani_df["MT_PARTNER"].astype(str) + "_" + pwani_df["BRANCH"].astype(str)

    # filter for brand and category
    if territory.lower() == "all":
        brand_df = pwani_df[pwani_df["BRAND"] == brand]
        if brand_df.empty:
            raise ValueError(f"Brand '{brand}' not found in data")

        if brand_df["CATEGORY"].empty:
            raise ValueError(f"No CATEGORY found for brand '{brand}'")

        category = brand_df["CATEGORY"].iloc[0]
        internal_comp = pwani_df[(pwani_df["CATEGORY"] == category) & (pwani_df["BRAND"] != brand)]
        comp_df = comp_df[comp_df["CATEGORY"] == category]

    else:
        brand_df = pwani_df[(pwani_df["BRAND"] == brand) & (pwani_df["TERRITORY"] == territory)]
        print(brand_df.shape)
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

    # merge all and engineer features
    combined = pd.concat([brand_df, internal_comp, comp_df], ignore_index=True)
    combined = new_columns(combined)

    # split back by source
    pwani_data = combined[(combined["BRAND"] == brand) & (combined["source"] == "pwani")]
    internal_comp = combined[(combined["BRAND"] != brand) & (combined["source"] == "pwani")]
    comp_data = combined[combined["source"] == "competitor"]

    analysis = MtAnalysis()

    return {
        "brand_name": brand,
        "territory": territory,
        "category": category,
        "overall_conclusion": analysis.overall_conclusion(pwani_data),
        "internal_competition": analysis.internal_comp_md(internal_comp),
        "external_competition": analysis.competitor_data_md(comp_data),
        "target_partner": analysis.partner_analysis_md(pwani_data),
        "internal_partner": analysis.partner_analysis_md(internal_comp),
        "external_partner": analysis.partner_analysis_md(comp_data),
        "target_sub_county": analysis.subcounty_analysis_md(pwani_data),
        "internal_sub_county": analysis.subcounty_analysis_md(internal_comp),
        "external_subcounty": analysis.subcounty_analysis_md(comp_data),
    }
