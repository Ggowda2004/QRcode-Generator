from fastapi import APIRouter, HTTPException
from app.schemas.text_schema import TextRequest
from app.services.qr import generate_qr_text
from app.utils.image import create_image_response
from app.utils.logger import logger

router = APIRouter(
    prefix="/text",
    tags=["QR - text"]
)

@router.post(
    "",
    summary="Generate QR code for a Text",
    response_description="PNG image of generated QR code"
)
def generate_text_qr(request: TextRequest):
    try:
        img = generate_qr_text(request.text)
        logger.info(f"Generating QR code for text: {request.text}")
        return create_image_response(img)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))