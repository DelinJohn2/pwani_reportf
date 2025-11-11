import pandas as pd
from loging import setup_logger

logger = setup_logger("IntelligenceMakerGT")


def intelligence_maker_gt(rtm_data, gt_data, competitor_data, brand, category, territory, threshold=0.90):
    try:
        logger.info("Generating intelligence for brand=%s, territory=%s", brand, territory)

        # --- RTM Filtering ---
        rtm_filtered = rtm_data[rtm_data['brand'] == brand]
        if territory.lower() != "all":
            rtm_filtered = rtm_filtered[rtm_filtered['territory'] == territory]

        filtered_rtm = (
            rtm_filtered
            .groupby('subcounty')
            .agg(
                brand=('brand', "first"),
                average_white_space=('aws', 'mean'),
                total_qty_kg=('qtyKgRtm', 'sum'),
                avg_volume=('volume', 'mean'),
                avg_whitespace_score=('whiteSpaceScore', 'mean')
            )
            .reset_index()
        )

        # Drop columns fully null
        filtered_rtm = filtered_rtm.dropna(axis=1, how='all')

        # --- GT Filtering ---
        gt_filtered = gt_data[(gt_data['brandName'] == brand) & (gt_data['category'] == category)]
        if territory.lower() != "all":
            gt_filtered = gt_filtered[gt_filtered['market'] == territory]

        gt_filtered = gt_filtered.dropna(axis=1, how='all')

        # --- Competitor Filtering ---
        comp_filtered = competitor_data[competitor_data['category'] == category]
        if territory.lower() != "all":
            comp_filtered = comp_filtered[comp_filtered['market'] == territory]

        cutoff = comp_filtered['marketShare'].quantile(threshold)
        filtered_comp = comp_filtered[comp_filtered['marketShare'] >= cutoff]
        filtered_comp=filtered_comp.drop('item',axis=1)

        filtered_comp = filtered_comp.dropna(axis=1, how='all')

        # --- Internal Competition (Same category, other brands) ---
        inter_filtered = gt_data[(gt_data['brandName'] != brand) & (gt_data['category'] == category)]
        if territory.lower() != "all":
            inter_filtered = inter_filtered[inter_filtered['market'] == territory]

        inter_filtered = inter_filtered.dropna(axis=1, how='all')

        # --- Demographics ---
        demograpic_description = {
            "nairobi": "Urban professionals, brand-conscious, convenience-focused, higher disposable income...",
            "central": "Mixed urban-rural, price-conscious, traditional values...",
            "coast": "Tourism-influenced, multicultural, Swahili-dominant...",
            "lake": "Rural-urban mix, fishing communities...",
            "rift valley": "Agricultural communities, seasonal income, bulk purchasing..."
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
