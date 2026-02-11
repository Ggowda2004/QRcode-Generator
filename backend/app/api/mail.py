from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import io

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


@router.get("", summary="Generate QR code for mail", response_description="PNG image of generated QR code")
def generate_mail_qr(email: str = Query(..., description="Valid email to encode in QR")):
    try:
        img = generate_qr_mail(email)
        return create_image_response(img)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )