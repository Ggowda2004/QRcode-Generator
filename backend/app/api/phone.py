from fastapi import APIRouter, HTTPException
from app.schemas.phone_schema import PhoneRequest
from app.services.qr import generate_qr_phone
from app.utils.image import create_image_response
from app.utils.logger import logger

router = APIRouter(
    prefix="/phone",
    tags=["QR - phone"]
)

@router.post(
    "",
    summary="Generate QR code for a Phone Number",
    response_description="PNG image of generated QR code"
)
def generate_phone_qr(request: PhoneRequest):
    try:
        img = generate_qr_phone(request.number)
        logger.info(f"Generating QR code for phone number: {request.number}")
        return create_image_response(img)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))