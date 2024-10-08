import grpc
from libs.protocols import url_shortener_pb2
from libs.protocols import url_shortener_pb2_grpc
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from config.config import settings
from pydantic import BaseModel
import logging

# Initialize FastAPI app
app = FastAPI()

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Log level set to INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format with timestamp and log level
)

class ShortenRequestModel(BaseModel):
    url: str
    expiration: int = None  # Optional field

# Function to set up gRPC channel and stub
async def get_grpc_stub():
    try:
        logging.info("Connecting to gRPC service at %s:%s", settings.grpc_host, settings.grpc_port)
        # Set up gRPC channel and stub
        channel = grpc.aio.insecure_channel(f'{settings.grpc_host}:{settings.grpc_port}')
        stub = url_shortener_pb2_grpc.URLShortenerStub(channel)
        # You can add health checks or connection checks if needed
        logging.info("Successfully connected to gRPC service.")
        return stub
    except Exception as e:
        logging.error("Failed to connect to gRPC service: %s", e)
        raise HTTPException(status_code=500, detail="Failed to connect to gRPC service") from e

@app.post("/url/shorten", response_model=None)
async def shorten_url(request: ShortenRequestModel):
    logging.info("Received request to shorten URL: %s", request.url)
    try:
        # Get gRPC stub
        stub = await get_grpc_stub()

        # Create and send the gRPC request
        grpc_request = url_shortener_pb2.ShortenRequest(
            original_url=request.url,
            expiration=request.expiration
        )
        grpc_response = await stub.Shorten(grpc_request)
        logging.info("Successfully shortened URL: %s -> %s", request.url, grpc_response.short_url)

        # Return the response
        return JSONResponse(content={"short_url": grpc_response.short_url})

    except grpc.RpcError as e:
        logging.error("gRPC call to shorten URL failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to shorten the URL") from e



@app.get("/r/{short_url}", response_model=None)
async def resolve_url(short_url: str):
    logging.info("Received request to resolve short URL: %s", short_url)
    try:
        # Get gRPC stub
        stub = await get_grpc_stub()

        # Create and send the gRPC request
        grpc_request = url_shortener_pb2.ResolveRequest(short_url=short_url)
        grpc_response = await stub.Resolve(grpc_request)
        logging.info("Resolved short URL: %s -> %s", short_url, grpc_response.original_url)

        if grpc_response.original_url:
            return RedirectResponse(url=grpc_response.original_url)
        else:
            logging.warning("Short URL not found: %s", short_url)
            raise HTTPException(status_code=404, detail="Short URL not found")

    except grpc.RpcError as e:
        logging.error("gRPC call to resolve URL failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to resolve the URL") from e

@app.get("/")
async def index():
    logging.info("Health check on the URL shortener service")
    return {"message": "URL Shortener is running!"}
