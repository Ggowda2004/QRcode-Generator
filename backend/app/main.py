from fastapi import FastAPI, Request
from app.api.url import router as url_router
from app.api.mail import router as mail_router
from app.api.wifi import router as wifi_router
from app.utils.logger import logger
from app.api.vcard import router as vcard_router
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
app = FastAPI()

# ---------------------------
# Global Rate Limiter Setup
# ---------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(
        "Rate limit exceeded for IP: %s on path: %s",
        request.client.host,
        request.url.path
    )
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down."},
    )

# Apply global rate limit (example: 100 requests per minute per IP)
@app.middleware("http")
async def global_rate_limit_middleware(request: Request, call_next):
    response = await limiter.limit("1/minute")(lambda req: call_next(req))(request)
    return response



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


@app.get("/")
def home_p():
    return {"Machi you are in home page"}

@app.get("/healthz")
def health():
    return {"status": "ok"}