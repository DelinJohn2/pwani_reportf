from data_fetcher import DataReaderGT
from data_intelligence import intelligence_maker_gt
from llm import load_llm_anthorpic
from pdf_saver import markdown_to_pdf
from utils import prepare_dashboard_gt
from logging.logger import setup_logger
from tenacity import retry, stop_after_attempt, wait_exponential


logger = setup_logger("ExecutiveReportGenerator")


# Retry wrapper for LLM invocation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def invoke_llm_with_retry(llm, prompt):
    return llm.invoke(prompt)


def executive_report_generator(brand: str, prompt_path='prompts/gt/executive_summary.md'):
    try:
        logger.info("Starting executive report generation for brand=%s", brand)

        # --- Fetch data ---
        reader = DataReaderGT()
        gt_data_p = reader.read_gt_pwani_data()
        gt_data_comp = reader.read_gt_competitor_data()
        rtm_data = reader.read_rtm_data()
        logger.info("Data fetched successfully for brand=%s", brand)

        # --- Generate intelligence ---
        intelligence = intelligence_maker_gt(rtm_data, gt_data_p, gt_data_comp, brand, territory='all')
        logger.info("Intelligence generated successfully for brand=%s", brand)

        # --- Prepare prompt ---
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        prompt = template.format(**intelligence)
        logger.info("Prompt prepared for LLM")

        # --- Load LLM ---
        llm = load_llm_anthorpic()
        logger.info("LLM loaded successfully")

        # --- Generate report with retry ---
        report = invoke_llm_with_retry(llm, prompt)
        logger.info("LLM report generated successfully")

        # --- Prepare dashboard ---
        file = prepare_dashboard_gt(report, brand)
        pdf_bytes = markdown_to_pdf(file)
        logger.info("PDF generated successfully for brand=%s", brand)

        return pdf_bytes

    except Exception:
        logger.exception("Failed to generate executive report for brand=%s", brand)
        raise
