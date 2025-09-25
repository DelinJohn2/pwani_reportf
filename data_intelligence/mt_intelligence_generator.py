import pandas as pd

from logging.logger import setup_logger

from .mt_intelligence_processor import MtAnalysis

logger = setup_logger("IntelligenceCreatorMT")


def intelligence_creator_mt(pwani_df, comp_df, brand, territory,category):
    try:
        logger.info("Generating MT intelligence for brand=%s, territory=%s", brand, territory)

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

            internal_comp = pwani_df[(pwani_df["CATEGORY"] == category) & (pwani_df["BRAND"] != brand)]
            comp_df = comp_df[comp_df["CATEGORY"] == category]

        else:
            brand_df = pwani_df[(pwani_df["BRAND"] == brand) & (pwani_df["TERRITORY"] == territory)]
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

        from .mt_intelligence_processor import new_columns
        combined = new_columns(combined)

        # split back by source
        pwani_data = combined[(combined["BRAND"] == brand) & (combined["source"] == "pwani")]
        internal_comp = combined[(combined["BRAND"] != brand) & (combined["source"] == "pwani")]
        comp_data = combined[combined["source"] == "competitor"]

        analysis = MtAnalysis()

        result = {
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

        logger.info("MT intelligence generation successful for brand=%s, territory=%s", brand, territory)
        return result

    except Exception:
        logger.exception("Error generating MT intelligence for brand=%s, territory=%s", brand, territory)
        raise
