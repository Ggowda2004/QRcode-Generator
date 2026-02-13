from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Tuple, Optional

# -------------------------
# Enums for choices
# -------------------------
class BoxPosition(str, Enum):
    a = "a"  # all 3
    b = "b"  # top-left
    c = "c"  # top-right
    d = "d"  # bottom-left

# -------------------------
# QR request schema
# -------------------------
class QRRequest(BaseModel):
    data: str = Field(..., description="Text or URL to encode in QR code")
    qr_fill: Tuple[int, int, int] = Field((0, 0, 0), description="RGB color for normal QR modules")
    box_color: Tuple[int, int, int] = Field((0, 0, 0), description="RGB color for the big boxes")
    box_position: BoxPosition = Field(BoxPosition.a, description="Which big boxes to color: a/b/c/d")
    # center_logo_path: Optional[str] = Field(None, description="Path to user's PNG logo (optional)")
    
    @model_validator(mode="after")
    def validate_colors(self):
        # Validate RGB tuples
        for color_name in ["qr_fill", "box_color"]:
            color = getattr(self, color_name)
            if len(color) != 3 or not all(0 <= c <= 255 for c in color):
                raise ValueError(f"{color_name} must be 3 integers between 0 and 255")
        
        # Center logo advisory
        # if self.center_logo_path and not self.center_logo_path.endswith(".png"):
        #     print("⚠️ Advisable: Use a PNG with transparency for the center logo.")
        
        return self