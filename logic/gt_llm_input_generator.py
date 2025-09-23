from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel,Field
from typing import TypedDict
from data_fetcher import DataReaderGT
from data_intelligence import intelligence_maker_gt
from llm import load_llm_anthorpic
from pdf_saver import markdown_to_pdf

class OutputType(str, Enum):
    text = "text"
    text_image = "text_image"
    image = "image"

class Demographics(TypedDict):
    age_range: str
    age_context: Dict[str, str]
    gender: List[str]
    gender_context: Dict[str, str]
    income: str
    income_context: Dict[str, str]
    region: str
    region_context: Dict[str, str]
    urban_or_rural: str
    urban_rural_context: Dict[str, str]

class CampaignSchema(TypedDict):
    product: str
    category: str
    sku: Optional[str]
    channel: str
    platform: str
    campaign_category: str
    campaign_type: str
    tone: str
    content_type: str
    language: str

    text_instructions: Optional[str] = Field(
        """This is a prompt for a text LLM to generate the campaign. Instructions should be based on input data, aligned with the platform, and appropriate 
        for the campaign type. Include all necessary details required for campaign generation."""
    )
    
    image_instructions: Optional[str] = Field(
        """This is a prompt for an image LLM. Instructions should be highly specific and descriptive, considering the demographics of the territory. 
        Focus on creating targeted marketing imagery to attract the audience and improve positioning and sales. 
        Never mention bulk packaging; focus only on product placement in the market.
        IMPORTANT RULE: Never mention SKU, pack size, or bulk packaging anywhere in your output. Do not include product weight, quantity, or packaging details. Only focus on marketing message, family context, and demographic targeting.
"""
    )

    demographics: Demographics
    history: Optional[str]
    output_type: OutputType

    



def llm_input_generator(territory: str, brand: str,prompt_path='prompts/gt/content_generation.md'):
    
    reader = DataReaderGT()
    gt_data_p = reader.read_gt_pwani_data()
    gt_data_comp = reader.read_gt_competitor_data()
    rtm_data = reader.read_rtm_data()
    intelligence = intelligence_maker_gt(rtm_data, gt_data_p, gt_data_comp, brand, territory)
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    prompt = template.format(**intelligence)
    llm = load_llm_anthorpic().with_structured_output(CampaignSchema)
    report = llm.invoke(prompt)
    return report
    
			
    