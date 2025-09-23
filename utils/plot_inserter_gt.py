
from typing import Callable, Dict
from visual_generator import GTDashboardGenerator
import io
import base64
import matplotlib.pyplot as plt

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

import re
import json
def extract_json_blocks_gt(text):
    """Extract and parse JSON code blocks from markdown text"""
    blocks = re.findall(r'```json(.*?)```', text, re.DOTALL | re.IGNORECASE)
    results = []
    for block in blocks:
        cleaned = re.sub(r'//.*', '', block)              # remove // comments
        cleaned = re.sub(r'(\d),(\d)', r'\1\2', cleaned)  # remove commas in numbers
        try:
            results.append({"valid": True, "json_dict": json.loads(cleaned.strip())})
        except Exception as e:
            results.append({"valid": False, "error": str(e)})
    # return only valid JSONs as list
    return [p['json_dict'] for p in results if p['valid']]

def get_plot_generator_gt(json_blocks, brand):
    vis = GTDashboardGenerator(json_blocks, brand)
    return {
        "Market Opportunity Analysis": vis.market_share_chart,
        "Territory Priority Ranking": vis.territory_priority_matrix,
        "Strategic Implementation Approach": vis.implementation_timeline,
        "90 Days Implementation": vis.investment_allocation,
        "Risk Assessment & Mitigation": vis.risk_assessment,
        "Financial Projections": vis.roi_progression
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

def prepare_dashboard_gt(output,brand):
	clean_text = remove_json_blocks(output.content)
	json_blocks = extract_json_blocks_gt(output.content)
	plots=get_plot_generator_gt(json_blocks[0],brand)
	file=insert_plots_after_headings(clean_text,plots)
	return file