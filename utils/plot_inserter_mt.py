import re
from typing import Dict, Callable
import io,base64
import matplotlib.pyplot as plt
from utils import extract_json_blocks
from visual_generator import MTDashboardFromAi, MTDashboardGenerator

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 encoded PNG."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f'<img src="data:image/png;base64,{encoded}" />'



def remove_json_blocks(text: str) -> str:
    """Remove ```json ... ``` blocks from AI output."""
    return re.sub(r"```json.*?```", "", text, flags=re.DOTALL)




def get_plot_generators(result, company_name, json_blocks) -> Dict[str, Callable]:
    """Initialize chart generators and return mapping of heading -> function."""
    v_ai = MTDashboardFromAi(json_blocks)
    v_data = MTDashboardGenerator(result, company_name)

    return {
        "Partner Performance Matrix": v_data.create_partner_performance_chart,
        "Geographic Opportunity Heatmap": v_ai.create_geographic_heatmap,
        "Competitive Displacement Opportunities": v_data.create_competitive_chart,
        "Investment Prioritization Framework": v_ai.create_investment_martix,
        "Cross-Partner Synergy Optimization": v_data.create_opportunity_matrix,
        "90-Day Implementation Roadmap": v_ai.create_growth_projection,
    }




def insert_plots_after_headings(text: str, plot_generators: Dict[str, Callable]) -> str:
    """Insert generated plots as base64 images after specific markdown headings."""

    def replacer(match):
        heading = match.group(2).strip()
        normalized = re.sub(r"^\d+\.\s*", "", heading).strip()  # remove leading numbers
        if normalized in plot_generators:
            fig = plot_generators[normalized]()  # generate chart
            img_html = fig_to_base64(fig)
            return f"{match.group(0)}\n\n{img_html}\n"
        return match.group(0)

    return re.sub(r"(##\s+)(.+)", replacer, text)




def prepare_dashboard_markdown_mt(output, result, company_name="AFRISENSE") -> str:
    """Prepare clean markdown with embedded charts."""
    raw_text = output.content
    clean_text = remove_json_blocks(raw_text)
    json_blocks = extract_json_blocks(raw_text)
    plot_generators = get_plot_generators(result, company_name, json_blocks)
    return insert_plots_after_headings(clean_text, plot_generators)