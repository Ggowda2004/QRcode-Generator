from fastapi import APIRouter, HTTPException
from app.schemas.vcard_schema import VcardRequest
from app.services.qr import generate_qr_vcard
from app.utils.image import create_image_response

router = APIRouter(
    prefix="/vcard",
    tags=["QR - vcard"]
)

@router.post(
    "",
    summary="Generate QR code for a vCard",
    response_description="PNG image of generated QR code"
)
def generate_vcard_qr(vcard: VcardRequest):
    try:
        img = generate_qr_vcard(vcard)
        return create_image_response(img)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )