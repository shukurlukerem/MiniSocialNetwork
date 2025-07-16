from fastapi import FastAPI
from api.v1.routes import auth_routes
from api.v1.routes import user_routes
from app.core.config import Base, engine
from fastapi_cache import FastAPICache
#from fastapi_cache.backends.redis import RedisBackend
import aioredis
from core.rate_limiter import init_rate_limiter
from api.v1.routes import post_routers 
from fastapi import FastAPI, Request
from core.log import logger

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Mini Social Network",
    description="FastAPI Swagger test tətbiqi",
    version="1.0.0",
    docs_url="/docs",         
    redoc_url="/redoc",       
    openapi_url="/openapi.json"
)


app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix= "/user", tags=["User"])
app.include_router(post_routers.router, prefix="/posts", tags=["Posts"])


@app.get("/test")
def test():
    return {"message": "OK"}

@app.on_event("startup")
async def startup():
    await init_rate_limiter()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response