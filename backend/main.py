from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io

from services.qr import generate_qr

app = FastAPI()


@app.get("/generate")
def generate(url: str):
    img = generate_qr(url)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")


@app.get("/healthz")
def health():
    return {"status": "ok"}