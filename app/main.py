import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
import sentry_sdk
from fastapi_versioning import VersionedFastAPI

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, UserAdmin
from app.bookings.router import router as router_bookings
from app.database import engine
from app.hotels.router import router as route_hotels
from app.images.router import router as router_images
from app.users.router import router as router_users
from app.logger import logger

sentry_sdk.init(
    dsn="https://a0001e51bab438080a6126e3b48a5007@o4506042726219776.ingest.sentry.io/4506042743652352",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(route_hotels)
app.include_router(router_images)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type", "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"
    ],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://localhost:6379",
        encoding="utf8",
        decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}',)

admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response

