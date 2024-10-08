from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
import logging  
from config.config import settings
from libs.url_shortener import URLShortener

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s" 
)

# Connect to Redis
redis_client = redis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", decode_responses=True)

# Connect to MongoDB
mongo_client = AsyncIOMotorClient(settings.mongo_url)
db = mongo_client.url_shortener
url_collection = db.urls

# Initialize the URLShortener library
url_shortener = URLShortener(mongo_collection=url_collection, redis_client=redis_client)

class ShortenRequest(BaseModel):
    url: str
    expiration: int = None


@app.get("/r/{short_url}")
async def resolve_url(short_url: str):
    original_url = await url_shortener.resolve_url(short_url)
    if original_url:
        return RedirectResponse(url=original_url)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")



@app.post("/url/shorten")
async def shorten_url(request: ShortenRequest):
    try:
        short_url = await url_shortener.shorten_url(request.url, request.expiration)
        full_shortened_url = f"{settings.base_url}/r/{short_url}"
        return {"short_url": full_shortened_url}
    except Exception as e:
        logging.error(f"Error shortening URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to shorten the URL")


@app.get("/")
async def index():
    logging.info("Health check on the URL shortener Service")
    return "Your Service is running!"