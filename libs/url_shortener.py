import hashlib
import string
import logging

# Base62 characters for encoding
BASE62 = string.ascii_letters + string.digits

class URLShortener:
    def __init__(self, mongo_collection, redis_client):
        self.mongo_collection = mongo_collection
        self.redis_client = redis_client

    # Function to encode an integer into Base62
    def base62_encode(self, num: int) -> str:
        if num == 0:
            return BASE62[0]
        
        encoded_str = []
        base = len(BASE62)

        while num:
            num, rem = divmod(num, base)
            encoded_str.append(BASE62[rem])
        
        return ''.join(reversed(encoded_str))

    def generate_short_url(self, original_url: str) -> str:
        url_hash = hashlib.md5(original_url.encode()).hexdigest()  # Generate an MD5 hash of the URL

        # Convert part of the hash to an integer, then encode it in Base62
        url_id = int(url_hash, 16) % (10**9)
        short_url = self.base62_encode(url_id)

        logging.info("Generated short URL: %s for original URL: %s", short_url, original_url) 
        return short_url
  
    async def shorten_url(self, original_url: str, expiration: int = None) -> str:
        # Check if the short URL already exists in Redis
        cached_url = await self.redis_client.get(original_url)
        if cached_url:
            return cached_url

        # If not found in Redis, check MongoDB
        existing_url = await self.mongo_collection.find_one({"original_url": original_url})
        if existing_url:
            return existing_url["short_url"]

        # Generate a new short URL
        short_url = self.generate_short_url(original_url)

        # Prepare the data to store in MongoDB
        url_data = {
            "short_url": short_url,
            "original_url": original_url,
            "expiration": expiration
        }

        await self.mongo_collection.insert_one(url_data)
        await self.redis_client.set(short_url, original_url, ex=expiration)
            
        return short_url

    async def resolve_url(self, short_url: str) -> str:
        # Check if the short URL already exists in Redis
        cached_url = await self.redis_client.get(short_url)
        if cached_url:
            return cached_url

        # If not found in Redis, check MongoDB
        existing_url = await self.mongo_collection.find_one({"short_url": short_url})
        if existing_url:
            return existing_url["original_url"]
        return None