from data_fetcher import DataReaderGT
from data_intelligence import intelligence_maker_gt
from llm import load_llm_anthorpic
from pdf_saver import markdown_to_pdf
from loging.logger import setup_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = setup_logger("TerritoryReportGenerator")

# Retry wrapper for LLM invocation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def invoke_llm_with_retry(llm, prompt):
    logger.info("Invoking LLM...")
    result = llm.invoke(prompt)
    logger.info("LLM invocation successful")
    return result

def territory_report_generator(territory: str, brand: str,category:str, prompt_path='prompts/gt/territory_analysis.md'):
    try:
        logger.info("Starting territory report generation for brand=%s, territory=%s", brand, territory)

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

        # --- Load LLM ---
        llm = load_llm_anthorpic()
        logger.info("LLM loaded successfully")

        # --- Invoke LLM with retry ---
        report = invoke_llm_with_retry(llm, prompt)

        # --- Convert report to PDF ---
        pdf_bytes = markdown_to_pdf(report.content)
        logger.info("PDF generated successfully for brand=%s, territory=%s", brand, territory)

        return pdf_bytes

    except Exception:
        logger.exception("Failed to generate territory report for brand=%s, territory=%s", brand, territory)
        raise
