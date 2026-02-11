from pydantic import BaseModel
from enum import Enum

class WifiSecurity(str, Enum):
    WPA = "WPA"
    WEP = "WEP"
    NOPASS = "nopass"


class wifi_s(BaseModel):
    security : WifiSecurity
    ssid : str
    password : str | None=None