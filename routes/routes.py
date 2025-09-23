from fastapi import APIRouter
from fastapi.responses import StreamingResponse,JSONResponse
from pydantic import BaseModel
from io import BytesIO
import time

from logic import MTReportGenerator, executive_report_generator, territory_report_generator,llm_input_generator

mt_report_gen = MTReportGenerator()
router = APIRouter()

# ----------------------------
# Request models
# ----------------------------
class BrandRequest(BaseModel):
    brand: str

class TerritoryRequest(BaseModel):
    brand: str
    territory: str


def create_pdf_response(pdf_bytes: bytes, filename: str):
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
       
    )


@router.post("/mt/executive_summary")
def mt_executive_summary(req: BrandRequest):
    pdf_bytes = mt_report_gen.generate_executive_summary(req.brand)

    return create_pdf_response(pdf_bytes, f"mt_executive_summary_{req.brand}")


@router.post("/mt/territory_report")
def mt_territory_report(req: TerritoryRequest):
    pdf_bytes = mt_report_gen.generate_territory_report(req.territory, req.brand)
   
    return create_pdf_response(pdf_bytes, f"mt_territory_{req.territory}_{req.brand}")


@router.post("/gt/executive_summary")
def gt_executive_summary(req: BrandRequest):
    pdf_bytes = executive_report_generator(req.brand)

    return create_pdf_response(pdf_bytes, f"gt_executive_summary_{req.brand}")

# ----------------------------
# GT Territory Report
# ----------------------------
@router.post("/gt/territory_report")
def gt_territory_report(req: TerritoryRequest):
    pdf_bytes = territory_report_generator(req.territory, req.brand)
    return create_pdf_response(pdf_bytes, f"gt_territory_{req.territory}_{req.brand}")

@router.post('/gt/llm_input')
def gt_llm_input(req:TerritoryRequest):
    output=llm_input_generator(req.territory,req.brand)
    return JSONResponse(output)
