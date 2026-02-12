from fastapi import HTTPException, APIRouter
from app.schemas.wifi_schema import WifiRequest
from app.services.qr import generate_qr_wifi
from app.utils.image import create_image_response
from app.utils.logger import logger


router = APIRouter(
    prefix="/wifi",
    tags=["QR-wifi"]
)

@router.post("", summary="Generate QR code for wifi", response_description="PNG image of generated QR code")
def generate_wifi_qr(data:WifiRequest):
    try:
        logger.info(f"Generating QR code for WiFi: SSID={data.ssid}, Security={data.security}")
        img = generate_qr_wifi(data.security, data.ssid, data.password)
        return create_image_response(img)
    except Exception as e:
        logger.error(f"Error generating QR code for WiFi: SSID={data.ssid}, Security={data.security}, error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )