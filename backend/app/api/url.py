from fastapi import APIRouter, HTTPException
from app.schemas.url_schema import UrlRequest
from app.services.qr import generate_qr_url
from app.utils.image import create_image_response

router = APIRouter(
    prefix="/url",
    tags=["QR - URL"]
)

@router.post(
    "",
    summary="Generate QR code for a URL",
    response_description="PNG image of generated QR code"
)
def generate_url_qr(url: UrlRequest):
    try:
        img = generate_qr_url(url)
        return create_image_response(img)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )