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
    The QR code is generated entirely in-memory and returned as a PNG image response.
    """
    try:
        # Parse RGB strings into tuples
        qr_fill_tuple = tuple(int(c.strip()) for c in qr_fill.split(","))
        box_color_tuple = tuple(int(c.strip()) for c in box_color.split(","))

        # When a user uploads a file, it arrives at your server as a stream of binary data (0s and 1s) over an HTTP connection. ->FastAPI (or similar) intercepts these bytes ->The center_logo.file you used is simply a "handle" or a pointer to the start of that memory slice.
        #When you run Image.open(center_logo.file), Pillow doesn't look for a file on your hard drive. Instead: It reads the bytes directly from the memory buffer,-> finally The Extraction: When you add .convert("RGBA"), Pillow "unpacks" the compressed image data (like ZIP) into a raw pixel map (Red, Green, Blue, Alpha) in a new section of your RAM.
        #In Python, an object exists in the Heap (RAM).As long as your API request is "alive," that memory is reserved. Once the request finishes and the response is sent, Python's Garbage Collector sees that no one is using that Image object anymore and clears that RAM for the next user.


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