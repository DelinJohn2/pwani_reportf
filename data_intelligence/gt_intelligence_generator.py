import pandas as pd
from loging.logger import setup_logger


logger = setup_logger("IntelligenceMakerGT")



def intelligence_maker_gt(rtm_data, gt_data, competitor_data, brand, category ,territory,threshold=0.05):
    try:
        logger.info("Generating intelligence for brand=%s, territory=%s", brand, territory)

        # --- RTM Filtering ---
        rtm_filtered = rtm_data[rtm_data['BRAND'] == brand]
        if territory.lower() != "all":
            rtm_filtered = rtm_filtered[rtm_filtered['TERRITORY'] == territory]

        filtered_rtm = (
            rtm_filtered
            .groupby('SUB_COUNTY')
            .agg(
                brand=('BRAND', "first"),
                average_white_space=('AWS_NEW', 'mean'),
                total_qty_kg=('QTY_KG_RTM', 'sum'),
                avg_norm_qty=('QTY_KG_RTM_NORM_BRANDWISE', 'mean'),
                avg_region_share=('QTY_SHARE_REGION_BRAND', 'mean'),
                avg_whitespace_score=('WHITE_SPACE_SCORE_TERRITORY', 'mean')
            )
            .reset_index()
        )

        # --- GT Filtering ---
        gt_filtered = gt_data[gt_data['brandName'] == brand]
        if territory.lower() != "all":
            gt_filtered = gt_filtered[gt_filtered['market'] == territory]

       

        # --- Competitor Filtering ---
        comp_filtered = competitor_data[competitor_data['category'] == category]
        if territory.lower() != "all":
            comp_filtered = comp_filtered[comp_filtered['market'] == territory]
        filtered_comp = comp_filtered[comp_filtered['marketShare'] >= threshold]

        inter_filtered = gt_data[(gt_data['brandName'] != brand) & (gt_data['category'] == category)]
        if territory.lower() != "all":
            inter_filtered = inter_filtered[inter_filtered['market'] == territory]

        # --- Demographics ---
        demograpic_description = {
            "nairobi": "Urban professionals, brand-conscious, convenience-focused, higher disposable income, tech-savvy, English/Swahili preference, modern retail shopping, premium positioning responsive, time-poor consumers, apartment living constraints, status-conscious purchasing",
            "central": "Mixed urban-rural, price-conscious, traditional values, family-oriented purchasing, quality-focused, agricultural communities, seasonal income patterns, local language important (Kikuyu), extended family influence, bulk purchasing preferences",
            "coast": "Tourism-influenced, multicultural, humid climate considerations, Swahili-dominant, seasonal business patterns, imported goods exposure, unique  challenges (climate factors), beach lifestyle impact, hospitality industry presence",
            "lake": "Rural-urban mix, fishing communities, water abundance, community-oriented, price-sensitive, traditional retail dominance, local cultural practices influence , word-of-mouth marketing effective, cooperative purchasing patterns",
            "rift valley": "Agricultural communities, seasonal income, large households, bulk purchasing, pastoralist influence, resource scarcity concerns, community word-of-mouth important, diverse ethnic groups, farming calendar impacts, livestock considerations",
        }

        result = {
            'brand_name': brand,
            'category': category,
            'territory': territory,
            'rtm_data': filtered_rtm.to_csv(index=False),
            'gt_data': gt_filtered.to_csv(index=False),
            'external_comp': filtered_comp.to_csv(index=False),
            'internal_comp': inter_filtered.to_csv(index=False),
            'territory_demographic': demograpic_description.get(territory) if territory != 'all' else demograpic_description
        }

        logger.info("Intelligence generation successful for brand=%s, territory=%s", brand, territory)
        return result

    except Exception as e:
        logger.exception("Error generating intelligence for brand=%s, territory=%s", brand, territory)
        raise
