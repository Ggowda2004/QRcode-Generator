from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.url import router as url_router
from app.api.mail import router as mail_router
from app.api.wifi import router as wifi_router
from app.api.vcard import router as vcard_router
from app.api.custom import router as custom_qr_router
from app.utils.logger import logger
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI()

# ---------------------------
# Global Rate Limiter Setup
# ---------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down."},
    )


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

app.include_router(vcard_router , prefix="/api/v1/qr")

app.include_router(custom_qr_router, prefix="/api/v1/qr")

@app.get("/")
def home_p():
    return {"Machi you are in home page"}

@app.get("/healthz")
def health():
    return {"status": "ok"}