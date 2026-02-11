from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
from app.services.qr import generate_qr_mail, generate_qr_wifi
from app.api.url import router as url_router
from app.api.mail import router as mail_router
from app.api.wifi import router as wifi_router
app = FastAPI()

app.include_router(url_router, prefix="/api/v1/qr")

app.include_router(mail_router,prefix="/api/v1/qr")

app.include_router(wifi_router, prefix="/api/v1/qr")



@app.get("/healthz")
def health():
    return {"status": "ok"}