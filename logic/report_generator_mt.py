from data_intelligence import intelligence_creator_mt
from utils import prepare_dashboard_markdown_mt
from data_fetcher import DataReaderMt
from llm import load_llm_anthorpic
from pdf_saver import markdown_to_pdf


class MTReportGenerator:
    def __init__(self):
        """Initialize data reader and LLM."""
        self.reader = DataReaderMt()
        self.llm = load_llm_anthorpic()

    def _clean_brand_column(self, df):
        """Ensure BRAND column has no spaces."""
        df['BRAND'] = df['BRAND'].str.replace(" ", "", regex=False)
        return df

    def _get_base_data(self):
        """Fetch and clean Pwani + competitor datasets."""
        pwani_data = self._clean_brand_column(self.reader.read_mt_pwani_data())
        competitor_data = self.reader.read_mt_competitor_data()
        return pwani_data, competitor_data

    def generate_territory_report(self, territory: str, brand: str, prompt_path: str = "prompts/mt/territory_report.md") -> str:
        """Generate a PDF report for a given brand in a territory."""
        pwani_data, competitor_data = self._get_base_data()

        result = intelligence_creator_mt(pwani_data, competitor_data, brand, territory)

        with open(prompt_path, "r") as f:
            prompt = f.read()

        final_prompt = prompt.format(**result)
        llm_result = self.llm.invoke(final_prompt)

        # return markdown_to_pdf(llm_result.content)
        return llm_result.content

    def generate_executive_summary(self, brand: str, prompt_path: str = "prompts/mt/executive_summary.md"):
        """Generate an executive summary PDF with charts for a brand."""
        pwani_data, competitor_data = self._get_base_data()

        result = intelligence_creator_mt(pwani_data, competitor_data, brand, territory="all")

        with open(prompt_path, "r") as f:
            prompt = f.read()

        final_prompt = prompt.format(**result)
        llm_result = self.llm.invoke(final_prompt)

        md_with_charts = prepare_dashboard_markdown_mt(llm_result, result, brand)
        return markdown_to_pdf(md_with_charts)
        return llm_result

