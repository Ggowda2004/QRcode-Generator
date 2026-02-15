from fastapi import APIRouter, HTTPException
from app.schemas.url_schema import UrlRequest
from app.services.qr import generate_qr_url
from app.utils.image import create_image_response
from app.utils.logger import logger
router = APIRouter(
    prefix="/url",#prepends with every path dedfined by this router
    tags=["QR - URL"]#used in documentation in swagger
)

#By setting the path to an empty string, this endpoint becomes the root of the combined prefixes you've already defined.
#summary for swagger ui for readability
#response_description for swagger ui to describe the response content.
@router.post(
    "",
    summary="Generate QR code for a URL",
    response_description="PNG image of generated QR code"
)
def generate_url_qr(url: UrlRequest):
    try:
        img = generate_qr_url(url)
        logger.info(f"Generating QR code for URL: {url.url}")
        return create_image_response(img)
    except Exception as e:
        logger.error(f"Error generating QR code for URL: {url.url}, error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )