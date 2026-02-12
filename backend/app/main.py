from fastapi import FastAPI, Request
from app.api.url import router as url_router
from app.api.mail import router as mail_router
from app.api.wifi import router as wifi_router
from app.utils.logger import logger
app = FastAPI()

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    log_dict={
        "url":request.url.path,
        "method":request.method,   
    }
    logger.info(log_dict)
    response= await call_next(request)
    return response

app.include_router(url_router, prefix="/api/v1/qr")

app.include_router(mail_router,prefix="/api/v1/qr")

app.include_router(wifi_router, prefix="/api/v1/qr")


@app.get("/")
def home_p():
    return {"Machi you are in home page"}

@app.get("/healthz")
def health():
    return {"status": "ok"}