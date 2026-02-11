from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import io
from app.schemas.mail_schema import mail_s
from app.services.qr import generate_qr_mail

router = APIRouter(
    prefix="/mail",
    tags=["QR - mail"]
)

def create_image_response(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")


@router.post("", summary="Generate QR code for mail", response_description="PNG image of generated QR code")
def generate_mail_qr(mail:mail_s):
    try:
        img = generate_qr_mail(mail)
        return create_image_response(img)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )