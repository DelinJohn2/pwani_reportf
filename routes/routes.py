from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from io import BytesIO
import time
from loging.logger import setup_logger

from logic import MTReportGenerator, executive_report_generator, territory_report_generator, llm_input_generator

logger = setup_logger("FastAPIReports")

mt_report_gen = MTReportGenerator()
router = APIRouter()

# ----------------------------
# Request models
# ----------------------------
class BrandRequest(BaseModel):
    brand: str
    category:str
class TerritoryRequest(BaseModel):
    brand: str
    territory: str
    category:str


def create_pdf_response(pdf_bytes: bytes, filename: str):
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
    )


@router.post("/mt/executive_summary")
def mt_executive_summary(req: BrandRequest):
    try:
        logger.info("Generating MT executive summary for brand=%s", req.brand)
        pdf_bytes = mt_report_gen.generate_executive_summary(req.brand,req.category)
        logger.info("MT executive summary generated successfully for brand=%s", req.brand)
        return create_pdf_response(pdf_bytes, f"mt_executive_summary_{req.brand}")
    except Exception:
        logger.exception("Failed to generate MT executive summary for brand=%s", req.brand)
        raise


@router.post("/mt/territory_report")
def mt_territory_report(req: TerritoryRequest):
    try:
        logger.info("Generating MT territory report for brand=%s, territory=%s", req.brand, req.territory,req.category)
        pdf_bytes = mt_report_gen.generate_territory_report(req.territory, req.brand)
        logger.info("MT territory report generated successfully for brand=%s, territory=%s", req.brand, req.territory)
        return create_pdf_response(pdf_bytes, f"mt_territory_{req.territory}_{req.brand}")
    except Exception:
        logger.exception("Failed to generate MT territory report for brand=%s, territory=%s", req.brand, req.territory)
        raise


@router.post("/gt/executive_summary")
def gt_executive_summary(req: BrandRequest):
    try:
        logger.info("Generating GT executive summary for brand=%s", req.brand)
        pdf_bytes = executive_report_generator(req.brand,req.category)
        logger.info("GT executive summary generated successfully for brand=%s", req.brand)
        return create_pdf_response(pdf_bytes, f"gt_executive_summary_{req.brand}")
    except Exception:
        logger.exception("Failed to generate GT executive summary for brand=%s", req.brand)
        raise


@router.post("/gt/territory_report")
def gt_territory_report(req: TerritoryRequest):
    try:
        logger.info("Generating GT territory report for brand=%s, territory=%s", req.brand, req.territory)
        pdf_bytes = territory_report_generator(req.territory, req.brand,req.category)
        logger.info("GT territory report generated successfully for brand=%s, territory=%s", req.brand, req.territory)
        return create_pdf_response(pdf_bytes, f"gt_territory_{req.territory}_{req.brand}")
    except Exception:
        logger.exception("Failed to generate GT territory report for brand=%s, territory=%s", req.brand, req.territory)
        raise


@router.post('/gt/llm_input')
def gt_llm_input(req: TerritoryRequest):
    try:
        logger.info("Generating GT LLM input for brand=%s, territory=%s", req.brand, req.territory)
        output = llm_input_generator(req.territory, req.brand,req.category)
        logger.info("GT LLM input generated successfully for brand=%s, territory=%s", req.brand, req.territory)
        return JSONResponse(output)
    except Exception:
        logger.exception("Failed to generate GT LLM input for brand=%s, territory=%s", req.brand, req.territory)
        raise
