import qrcode
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
def generate_qr_url(data: str):
    return generate_qr_image(data)

#2
def generate_qr_mail(email: str):
    return generate_qr_image(f"mailto:{email}")

#3 (escape sequence with required func)
def escape_wifi(value: str) -> str:
    #Escapes special characters \, ;, ,, and : as required by MECARD/WiFi standards.
    # Order matters: backslash must be escaped first
    for char in ["\\", ";", ",", ":", '"']:
        value = value.replace(char, f"\\{char}")
    return value
def generate_qr_wifi(security: str, ssid: str, password: str=""):
    ssid = escape_wifi(ssid)
    password=escape_wifi(password)

    security=security.upper()
    if security=="NOPASS":
        wifi_link= f"WIFI:S:{ssid};T:nopass;;"
    else:
        wifi_link=f"WIFI:S:{ssid};T:{security};P:{password};;"

    return generate_qr_image(wifi_link)