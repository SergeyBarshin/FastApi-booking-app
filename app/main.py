from fastapi import FastAPI, Query
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as route_hotels
from app.images.router import router as router_images

from redis import asyncio as aioredis


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
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")