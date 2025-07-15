from fastapi import FastAPI
from app.api.v1.routes import auth_routes
from app.api.v1.routes import user_routes
from app.core.config import Base, engine
from fastapi_cache import FastAPICache
#from fastapi_cache.backends.redis import RedisBackend
import aioredis
from app.core.rate_limiter import init_rate_limiter
from app.api.v1.routes import post_routers 

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