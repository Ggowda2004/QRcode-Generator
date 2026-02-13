from fastapi import APIRouter, HTTPException, UploadFile, Form
from app.schemas.custom_schema import BoxPosition
from app.services.custom_qr import generate_qr_image
from app.utils.image import create_image_response
from app.utils.logger import logger
from typing import Optional
from PIL import Image

router = APIRouter(
    prefix="/custom-qr",
    tags=["QR - Custom"]
)

@router.post("", summary="Generate custom QR code", response_description="PNG image of generated QR code")
async def generate_custom_qr(
    data: str = Form(..., description="Text or URL for QR code"),
    qr_fill: str = Form("0,0,0", description="RGB color for normal modules, e.g., 0,0,0"),
    box_color: str = Form("0,0,0", description="RGB color for big boxes, e.g., 255,0,0"),
    box_position: BoxPosition = Form(BoxPosition.a, description="Which big boxes to color"),
    center_logo: Optional[UploadFile] = None
):
    """
    Generates a QR code with:
    - Custom colors
    - Custom big box selection
    - User-provided center logo (PNG)
    - Default company logo at the bottom
    """
    try:
        # Parse RGB strings into tuples
        qr_fill_tuple = tuple(int(c.strip()) for c in qr_fill.split(","))
        box_color_tuple = tuple(int(c.strip()) for c in box_color.split(","))

        # Save center logo temporarily if uploaded
        center_logo_img: Optional[Image.Image] = None
        if center_logo:
            center_logo_img = Image.open(center_logo.file).convert("RGBA")
        

        # Path to your default company logo
        bottom_logo_path = "app/assets/company_logo.png"

        # Generate QR image
        img: Image.Image = generate_qr_image(
            data=data,
            qr_fill=qr_fill_tuple,
            box_color=box_color_tuple,
            box_position=box_position,
            center_logo_img=center_logo_img,
            bottom_logo_path=bottom_logo_path
        )

        return create_image_response(img)

    except Exception as e:
        logger.error("Error generating custom QR code: %s", str(e))
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate QR code: {str(e)}"
        )