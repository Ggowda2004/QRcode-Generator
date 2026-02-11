from fastapi import HTTPException, APIRouter, Query
import io
from fastapi.responses import StreamingResponse

from app.services.qr import generate_qr_wifi

router = APIRouter(
    prefix="/wifi",
    tags=["QR-wifi"]
)

def create_image_response(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

@router.get("", summary="Generate QR code for wifi", response_description="PNG image of generated QR code")
def generate_wifi_qr(security: str, ssid: str, password: str=""):
    try:
        img = generate_qr_wifi(security, ssid, password)
        return create_image_response(img)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )