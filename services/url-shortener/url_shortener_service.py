from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
import hashlib
import string
import logging  
from config.config import settings

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s" 
)

# Connect to Redis asynchronously
@app.on_event("startup")
async def connect_redis():
    app.state.redis = await redis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", encoding="utf-8", decode_responses=True)

# Connect to MongoDB
mongo_client = AsyncIOMotorClient(settings.mongo_url)
db = mongo_client.url_shortener
url_collection = db.urls

# Base62 characters for encoding
BASE62 = string.ascii_letters + string.digits

class ShortenRequest(BaseModel):
    url: str
    expiration: int = None

class ResolveRequest(BaseModel):
    short_url: str


# Function to encode an integer into Base62
def base62_encode(num: int) -> str:
    if num == 0:
        return BASE62[0]
    
    encoded_str = []
    base = len(BASE62)

    while num:
        num, rem = divmod(num, base)
        encoded_str.append(BASE62[rem])
    
    return ''.join(reversed(encoded_str))


def generate_short_url(original_url: str) -> str:
    logging.info("Generating short URL for: %s", original_url)

    url_hash = hashlib.md5(original_url.encode()).hexdigest()  # Generate an MD5 hash of the URL

    # Convert part of the hash to an integer, then encode it in Base62
    url_id = int(url_hash, 16) % (10**9)
    short_url = base62_encode(url_id)

    logging.info("Generated short URL: %s for original URL: %s", short_url, original_url) 
    return short_url


@app.get("/r/{short_url}")
async def resolve_url(short_url: str):
    logging.info("URL Received request to resolve URL: %s", short_url)

    redis_client = app.state.redis

    # Check if the short URL exists in Redis
    cached_url = await redis_client.get(short_url)
    if cached_url:
        logging.info(f"URL found in Redis: {cached_url}")
        return {"original_url": cached_url}


    # If not found in Redis, check MongoDB
    existing_url = await url_collection.find_one({"short_url": short_url})
    logging.info("MongoDB query result for existing URL: %s", existing_url)

    if existing_url:
        original_url = existing_url["original_url"]
        logging.info("Resolved original URL: %s", original_url)

        # Cache the URL in Redis for future lookups
        await redis_client.set(short_url, original_url)
        logging.info(f"Stored resolved URL in Redis: {original_url}")

        return {"original_url": original_url}
    else:
        logging.warning("Short URL not found: %s", short_url)
        raise HTTPException(status_code =404, detail="Short URL is unknown")



@app.post("/url/shorten")
async def shorten_url(request: ShortenRequest):
    logging.info("Received request to shorten URL: %s", request.url)  

    redis_client = app.state.redis

    # Check if the short URL already exists in Redis
    cached_url = await redis_client.get(request.url)
    if cached_url:
        logging.info(f"URL found in Redis: {cached_url}")
        return {"short_url": cached_url}

    # If not found in Redis, check MongoDB
    existing_url = await url_collection.find_one({"original_url": request.url})
    logging.info("MongoDB query result for existing URL: %s", existing_url) 

    if existing_url:
        short_url = existing_url["short_url"]
        logging.info("URL already exists. Returning existing short URL: %s", short_url)  
        return {"short_url": short_url}

    # Generate a new short URL
    short_url = generate_short_url(request.url)

    # Prepare the data to store in MongoDB
    url_data = {
        "short_url": short_url,
        "original_url": request.url,
        "expiration": request.expiration
    }

    url_collection.insert_one(url_data)
    logging.info("Inserted new URL data into MongoDB: %s", url_data)  

    # Set the short URL in Redis with expiration
    redis_client.set(short_url, request.url, ex=request.expiration)
    logging.info("Stored short URL in Redis with expiration: %s seconds", request.expiration) 

    return {"short_url": short_url}

    
@app.get("/")
async def index():
    logging.info("Health check on the URL shortener Service")
    return "Your Service is running!"
