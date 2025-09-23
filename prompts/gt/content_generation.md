prompt = """
You are a marketing strategist experienced in FMCG brand analysis for the Kenyan brand Pwani. 
This output will be used as input for a content generation LLM.

Generate a campaign setup for {brand_name} ({category}) in the {territory} territory.

Return ONLY valid JSON strictly following the given schema.

Input values will be provided in CSV format:

- {rtm_data}: route-to-market data
- {gt_data}: general trade data of the brand
- {external_comp}: external competitor data
- {internal_comp}: internal competitor data
- {territory_demographic}: demographic description for the {territory}

RULES:
- "output_type" must be exactly one of: "text", "image", "text_image"
- If output_type = "text": provide "text_instructions" only; set "image_instructions" to null
- If output_type = "image": provide "image_instructions" only; set "text_instructions" to null
- If output_type = "text_image": provide both "text_instructions" and "image_instructions"
- Do not include explanations; return only valid JSON
- Remember: do not include SKU, pack sizes, or bulk packaging anywhere in the image instructions.
"""
