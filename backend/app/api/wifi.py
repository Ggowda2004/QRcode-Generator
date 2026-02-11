from fastapi import HTTPException, APIRouter
import io
from fastapi.responses import StreamingResponse
from app.schemas.wifi_schema import wifi_s
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

@router.post("", summary="Generate QR code for wifi", response_description="PNG image of generated QR code")
def generate_wifi_qr(data:wifi_s):
    try:
        img = generate_qr_wifi(data.security, data.ssid, data.password)
        return create_image_response(img)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )