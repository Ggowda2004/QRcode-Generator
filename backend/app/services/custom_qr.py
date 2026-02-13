from typing import Optional
import qrcode
from PIL import Image, ImageDraw
from app.schemas.custom_schema import BoxPosition
from app.utils.logger import logger

def generate_qr_image(
    data: str,
    qr_fill=(0,0,0),
    box_color=(0,0,0),
    box_position: BoxPosition=BoxPosition.a,
    center_logo_img: Optional[Image.Image] = None,
    bottom_logo_path: Optional[str] = None
):
    # Step 1: Build QR
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    matrix_size = len(matrix)
    border = qr.border
    box_size = 20
    img_size = matrix_size * box_size

    img = Image.new("RGBA", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    # Step 2: Draw modules
    for y in range(matrix_size):
        for x in range(matrix_size):
            if matrix[y][x]:
                in_box = False
                if box_position in ["a","b"] and border <= x < border+7 and border <= y < border+7:
                    in_box = True
                elif box_position in ["a","c"] and matrix_size-border-7 <= x < matrix_size-border and border <= y < border+7:
                    in_box = True
                elif box_position in ["a","d"] and border <= x < border+7 and matrix_size-border-7 <= y < matrix_size-border:
                    in_box = True

                color = box_color if in_box else qr_fill
                rect = [x*box_size, y*box_size, (x+1)*box_size, (y+1)*box_size]
                draw.rectangle(rect, fill=color)

    # Step 3: Paste center logo
    if center_logo_img:
        try:
            logo_size = int(img_size * 0.2)
            logo = center_logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            mask = Image.new("L", (logo_size, logo_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0,0,logo_size,logo_size), fill=255)

            pos = ((img_size - logo_size)//2, (img_size - logo_size)//2)
            img.paste(logo, pos, logo)
        except Exception as e:
            logger.error(f"Error pasting center logo: {e}")

    # Step 4: Paste bottom logo (default company logo)
    if bottom_logo_path:
        try:
            logger.info(f"Loading bottom logo from: {bottom_logo_path}")
            bottom_logo = Image.open(bottom_logo_path).convert("RGBA")
            wm_width = int(img_size * 0.15)
            wm_ratio = bottom_logo.height / bottom_logo.width
            wm_height = int(wm_width * wm_ratio)
            bottom_logo = bottom_logo.resize((wm_width, wm_height), Image.Resampling.LANCZOS)

            margin = int(img_size * 0.03)
            wm_pos = ((img_size - wm_width)//2, img_size - wm_height - margin)
            img.paste(bottom_logo, wm_pos, bottom_logo)
        except Exception as e:
            logger.error(f"Error loading bottom logo: {e}")

    return img