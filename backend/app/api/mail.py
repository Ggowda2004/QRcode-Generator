from fastapi import APIRouter, HTTPException
from app.schemas.mail_schema import MailRequest
from app.services.qr import generate_qr_mail
from app.utils.image import create_image_response
from app.utils.logger import logger
router = APIRouter(
    prefix="/mail",
    tags=["QR - mail"]
)

@router.post("", summary="Generate QR code for mail", response_description="PNG image of generated QR code")
def generate_mail_qr(email:MailRequest):
    try:
        logger.info("Generating QR code for email: %s", email.email)
        img = generate_qr_mail(email)
        return create_image_response(img)
    except Exception as e:
        logger.error("Error generating QR code for email: %s, error: %s", email.email, str(e))
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )