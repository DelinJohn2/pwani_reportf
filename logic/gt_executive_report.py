from data_fetcher import DataReaderGT
from data_intelligence import intelligence_maker_gt
from llm import load_llm_anthorpic
from pdf_saver import markdown_to_pdf
from utils import prepare_dashboard_gt

def executive_report_generator(brand: str, prompt_path='prompts/gt/executive_summary.md'):
   
    reader = DataReaderGT()
    gt_data_p = reader.read_gt_pwani_data()
    gt_data_comp = reader.read_gt_competitor_data()
    rtm_data = reader.read_rtm_data()
    intelligence = intelligence_maker_gt(rtm_data, gt_data_p, gt_data_comp, brand , territory='all')
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    prompt = template.format(**intelligence)
    llm = load_llm_anthorpic()
    report = llm.invoke(prompt)
    file=prepare_dashboard_gt(report,brand)
    pdf_bytes = markdown_to_pdf(file)

    return report.content