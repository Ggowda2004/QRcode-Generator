import qrcode
from app.schemas.wifi_schema import WifiSecurity
def generate_qr_image(data: str):
    qr = qrcode.QRCode(
        version=None,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

#1
def generate_qr_text(text: str):
    return generate_qr_image(text)

#2
def generate_qr_phone(number: str):
    return generate_qr_image(f"tel:{number}")

#3
def generate_qr_url(url: str):
    url = str(url.url)   #handled by converting back to url string from HttpUrl object, this is usually done in the router layer, check out phone router for example
    return generate_qr_image(url)

#4
def generate_qr_mail(email: str):
    email=str(email.email)   #handled by converting back to email string from EmailStr object
    return generate_qr_image(f"mailto:{email}")

#5 (escape sequence with required func)
def escape_wifi(value: str) -> str:
    #Escapes special characters \, ;, ,, and : as required by MECARD/WiFi standards.
    # Order matters: backslash must be escaped first
    for char in ["\\", ";", ",", ":", '"']:
        value = value.replace(char, f"\\{char}")
    return value
def generate_qr_wifi(security: WifiSecurity, ssid: str, password: str |None=None):
    ssid = escape_wifi(ssid)

    if security == WifiSecurity.NOPASS:
        wifi_link= f"WIFI:S:{ssid};T:nopass;;"
    else:
        password = escape_wifi(password or "")
        wifi_link=f"WIFI:S:{ssid};T:{security.value};P:{password};;"

    return generate_qr_image(wifi_link)

#6
def escape_vcard(value: str) -> str:
    """Escapes special characters for vCard format"""
    if value is None:
        return ""
    # Escape backslash first, then semicolon and comma
    for char in ["\\", ";", ","]:
        value = value.replace(char, f"\\{char}")
    return value

def generate_qr_vcard(vcard_data):
    """
    Generates a vCard format QR code.
    Supports minimal vCard (name only) to full vCard with all details.
    
    Args:
        vcard_data: VcardRequest object with contact information
    """
    # Build vCard with BEGIN and VERSION
    vcard = "BEGIN:VCARD\r\nVERSION:3.0\r\n"
    
    # Full name (FN) - Required
    full_name = f"{escape_vcard(vcard_data.first_name)} {escape_vcard(vcard_data.last_name)}".strip()
    vcard += f"FN:{full_name}\r\n"
    
    # Structured name (N) - Required
    vcard += f"N:{escape_vcard(vcard_data.last_name)};{escape_vcard(vcard_data.first_name)};;;\r\n"
    
    # Phone number - Optional
    if vcard_data.phone:
        phone = escape_vcard(vcard_data.phone)
        vcard += f"TEL:{phone}\r\n"
    
    # Email - Optional
    if vcard_data.email:
        email = escape_vcard(vcard_data.email)
        vcard += f"EMAIL:{email}\r\n"
    
    # Organization - Optional
    if vcard_data.organization:
        org = escape_vcard(vcard_data.organization)
        vcard += f"ORG:{org}\r\n"
    
    # Title/Job - Optional
    if vcard_data.title:
        title = escape_vcard(vcard_data.title)
        vcard += f"TITLE:{title}\r\n"
    
    # URL - Optional
    if vcard_data.url:
        url = escape_vcard(vcard_data.url)
        vcard += f"URL:{url}\r\n"
    
    # Address - Optional
    if vcard_data.street or vcard_data.city or vcard_data.state or vcard_data.postal_code or vcard_data.country:
        street = escape_vcard(vcard_data.street or "")
        city = escape_vcard(vcard_data.city or "")
        state = escape_vcard(vcard_data.state or "")
        postal = escape_vcard(vcard_data.postal_code or "")
        country = escape_vcard(vcard_data.country or "")
        # ADR format: PO Box;Extended Address;Street;City;State;PostalCode;Country
        vcard += f"ADR:;;{street};{city};{state};{postal};{country}\r\n"
    
    # Note - Optional
    if vcard_data.note:
        note = escape_vcard(vcard_data.note)
        vcard += f"NOTE:{note}\r\n"
    
    # End vCard
    vcard += "END:VCARD"
    
    return generate_qr_image(vcard)