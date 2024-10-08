import grpc
from concurrent import futures
import time
import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
import libs.protocols.url_shortener_pb2_grpc as url_shortener_pb2_grpc
import libs.protocols.url_shortener_pb2 as url_shortener_pb2
from libs.url_shortener import URLShortener
from config.config import settings
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Log level set to INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format with timestamp and log level
)

class URLShortenerServicer(url_shortener_pb2_grpc.URLShortenerServicer):
    def __init__(self, mongo_collection, redis_client):
        self.shortener = URLShortener(mongo_collection, redis_client)
        logging.info("URLShortenerServicer initialized")  # Log initialization

    async def Shorten(self, request, context):
        logging.info("Received Shorten request for URL: %s", request.original_url)  # Log request
        short_url = await self.shortener.shorten_url(request.original_url, request.expiration)
        logging.info("Generated short URL: %s for original URL: %s", short_url, request.original_url)  # Log generated short URL
        return url_shortener_pb2.ShortenResponse(short_url=short_url)

    async def Resolve(self, request, context):
        logging.info("Received Resolve request for short URL: %s", request.short_url)  # Log request
        original_url = await self.shortener.resolve_url(request.short_url)
        if original_url:
            logging.info("Resolved short URL: %s to original URL: %s", request.short_url, original_url)  # Log resolved URL
            return url_shortener_pb2.ResolveResponse(original_url=original_url)
        logging.warning("Short URL not found: %s", request.short_url)  # Log if short URL not found
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Short URL not found')
        return url_shortener_pb2.ResolveResponse()

async def init_mongo():
    logging.info("Initializing MongoDB connection...")
    mongo_client = AsyncIOMotorClient(settings.mongo_url)
    db = mongo_client.url_shortener
    url_collection = db.urls
    logging.info("MongoDB connection established")
    return url_collection

async def init_redis():
    logging.info("Initializing Redis connection...")
    redis_client = await redis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", encoding="utf-8", decode_responses=True)
    logging.info("Redis connection established")
    return redis_client

async def serve():
    # Initialize MongoDB and Redis
    mongo_collection = await init_mongo()
    redis_client = await init_redis()

    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    url_shortener_pb2_grpc.add_URLShortenerServicer_to_server(
        URLShortenerServicer(mongo_collection, redis_client), server
    )
    server.add_insecure_port(f'{settings.grpc_host}:{settings.grpc_port}')
    server.start()
    logging.info(f"gRPC server started on {settings.grpc_host}:{settings.grpc_port}")
    try:
        while True:
            logging.info("gRPC server is running...")
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        logging.info("gRPC server is stopping...")
        server.stop(0)

if __name__ == "__main__":
    import asyncio
    logging.info("Running gRPC URL Shortener Service...")
    asyncio.run(serve())
