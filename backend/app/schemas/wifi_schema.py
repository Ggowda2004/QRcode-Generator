from pydantic import BaseModel, model_validator
from enum import Enum

class WifiSecurity(str, Enum):
    WPA = "WPA"
    WEP = "WEP"
    NOPASS = "nopass"


class WifiRequest(BaseModel):
    security : WifiSecurity
    ssid : str
    password : str | None=None


    @model_validator(mode="after")
    def validate_password_logic(self):
        if self.security == WifiSecurity.NOPASS:
            if self.password:
                raise ValueError("Password must not be provided when security is NOPASS")

        if self.security == WifiSecurity.WPA and len(self.password) < 8:
            raise ValueError("WPA password must be at least 8 characters")
        
        else:  # WPA or WEP
            if not self.password and not WifiSecurity.NOPASS:
                raise ValueError("Password is required for WPA/WEP security")

        return self