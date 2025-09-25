from data_intelligence import intelligence_creator_mt
from utils import prepare_dashboard_markdown_mt
from data_fetcher import DataReaderMt
from llm import load_llm_anthorpic
from pdf_saver import markdown_to_pdf
from logging.logger import setup_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = setup_logger("MTReportGenerator")


# Retry wrapper for LLM invocation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def invoke_llm_with_retry(llm, prompt):
    logger.info("Invoking LLM...")
    result = llm.invoke(prompt)
    logger.info("LLM invocation successful")
    return result


class MTReportGenerator:
    def __init__(self):
        """Initialize data reader and LLM."""
        self.reader = DataReaderMt()
        self.llm = load_llm_anthorpic()
        logger.info("MTReportGenerator initialized successfully")

    def _clean_brand_column(self, df):
        """Ensure BRAND column has no spaces."""
        df['BRAND'] = df['BRAND'].str.replace(" ", "", regex=False)
        return df

    def _get_base_data(self):
        """Fetch and clean Pwani + competitor datasets."""
        try:
            pwani_data = self._clean_brand_column(self.reader.read_mt_pwani_data())
            competitor_data = self.reader.read_mt_competitor_data()
            logger.info("Base MT data fetched successfully")
            return pwani_data, competitor_data
        except Exception:
            logger.exception("Failed to fetch MT base data")
            raise

    def generate_territory_report(self, territory: str, brand: str, prompt_path: str = "prompts/mt/territory_report.md") -> bytes:
        """Generate a PDF report for a given brand in a territory."""
        try:
            pwani_data, competitor_data = self._get_base_data()

            result = intelligence_creator_mt(pwani_data, competitor_data, brand, territory)
            logger.info("MT intelligence generated for brand=%s, territory=%s", brand, territory)

            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_template = f.read()
            prompt = prompt_template.format(**result)
            logger.info("Prompt prepared for LLM")

            llm_result = invoke_llm_with_retry(self.llm, prompt)
            logger.info("LLM invocation completed for territory report")

            # Return markdown content or PDF
            pdf_bytes = markdown_to_pdf(llm_result.content)
            logger.info("PDF generated successfully for brand=%s, territory=%s", brand, territory)
            return pdf_bytes

        except Exception:
            logger.exception("Failed to generate MT territory report for brand=%s, territory=%s", brand, territory)
            raise

    def generate_executive_summary(self, brand: str, prompt_path: str = "prompts/mt/executive_summary.md") -> bytes:
        """Generate an executive summary PDF with charts for a brand."""
        try:
            pwani_data, competitor_data = self._get_base_data()

            result = intelligence_creator_mt(pwani_data, competitor_data, brand, territory="all")
            logger.info("MT executive summary intelligence generated for brand=%s", brand)

            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_template = f.read()
            prompt = prompt_template.format(**result)
            logger.info("Prompt prepared for LLM")

            llm_result = invoke_llm_with_retry(self.llm, prompt)
            logger.info("LLM invocation completed for executive summary")

            md_with_charts = prepare_dashboard_markdown_mt(llm_result, result, brand)
            pdf_bytes = markdown_to_pdf(md_with_charts)
            logger.info("Executive summary PDF generated successfully for brand=%s", brand)
            return pdf_bytes

        except Exception:
            logger.exception("Failed to generate MT executive summary for brand=%s", brand)
            raise
