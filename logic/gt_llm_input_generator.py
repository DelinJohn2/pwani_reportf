from enum import Enum
from typing import Optional, List, Dict
from pydantic import Field
from typing import TypedDict
from data_fetcher import DataReaderGT
from data_intelligence import intelligence_maker_gt
from llm import load_llm_anthorpic
from pdf_saver import markdown_to_pdf
from loging.logger import setup_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = setup_logger("LLMInputGenerator")


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
        """This is a prompt for a text-based LLM to generate the campaign content.
        The instructions should be based on the input data and reflect the correct tone and audience for the product category.
        Make sure the style and message feel realistic and appropriate for that product.

        Examples:
        - Cooking oil: family warmth, healthy meals, everyday cooking joy.
        - Laundry bar: freshness, cleanliness, family care.
        - Toilet soap: luxury, self-care, comfort.
        - Handwash: hygiene, protection, personal safety.

        Never mention SKU, pack size, quantity, or bulk packaging.
        Focus only on messaging that suits the market and campaign objective.
        """
    )

    image_instructions: Optional[str] = Field(
        """This is a prompt for an image-generation LLM to create marketing visuals.
        The imagery should be specific, appealing, and consistent with the product type and audience.
        Always keep scenes realistic and brand-appropriate like if its luxury or economical.

        Examples:
        - Cooking oil: family cooking together or serving food.
        - Laundry bar: a homemaker with clean, fresh clothes.
        - Toilet soap: a woman in a bathrobe enjoying a private, luxurious bath.
        - Handwash: hands being washed at a sink, showing freshness and hygiene.

        IMPORTANT RULES:
        - Never include SKU, pack size, weight, or bulk packaging.
        - Do not show industrial, retail, or community settings.
        - Focus on lifestyle, emotion, and placement relevant to the product.
        """
    )
    demographics: Demographics
    history: Optional[str]
    output_type: OutputType


# Retry wrapper for LLM invocation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def invoke_llm_with_retry(llm, prompt):
    logger.info("Invoking LLM...")
    result = llm.invoke(prompt)
    logger.info("LLM invocation successful")
    return result


def llm_input_generator(territory: str, brand: str,category:str, prompt_path='prompts/gt/content_generation.md'):
    try:
        logger.info("Generating LLM input for brand=%s, territory=%s", brand, territory)

        # --- Fetch data ---
        reader = DataReaderGT()
        gt_data_p = reader.read_gt_pwani_data()
        gt_data_comp = reader.read_gt_competitor_data()
        rtm_data = reader.read_rtm_data()
        logger.info("Data fetched successfully for brand=%s, territory=%s", brand, territory)

        # --- Generate intelligence ---
        intelligence = intelligence_maker_gt(rtm_data, gt_data_p, gt_data_comp, brand, category,territory)
        logger.info("Intelligence generated successfully")

        # --- Prepare prompt ---
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        prompt = template.format(**intelligence)
        logger.info("Prompt prepared for LLM")

        # --- Load LLM with structured output ---
        llm = load_llm_anthorpic().with_structured_output(CampaignSchema)
        logger.info("LLM loaded successfully")

        # --- Invoke LLM with retry ---
        report = invoke_llm_with_retry(llm, prompt)

        logger.info("LLM input generation completed successfully for brand=%s, territory=%s", brand, territory)
        return report

    except Exception:
        logger.exception("Failed to generate LLM input for brand=%s, territory=%s", brand, territory)
        raise
