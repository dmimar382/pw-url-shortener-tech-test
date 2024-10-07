import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from config.config import settings
import requests

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()
BASE_URL: str = "http://localhost:8000"


class ShortenRequest(BaseModel):
    url: str


@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
    Forward the request to the URL shortener service to generate a shortened URL.
    """
    logging.info("Received request to shorten URL: %s", request.url)
    
    try:
        # Forward the request to the url-shortener service
        response = requests.post(f"{settings.url_shortener_service}/url/shorten", json=request.dict())
        logging.info("Forwarded request to url-shortener service: %s", response.url)
        response.raise_for_status()

        shortened_url = response.json().get("short_url")
        logging.info("Shortened URL received: %s", shortened_url)

        full_shortened_url = f"{BASE_URL}/r/{shortened_url}"
        
        return {"short_url": full_shortened_url}
    except requests.exceptions.RequestException as e:
        logging.error("Error shortening the URL: %s", e)
        raise HTTPException(status_code=500, detail="Failed to shorten the URL") from e


@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Forward the request to the URL shortener service to resolve the shortened URL.
    """
    logging.info("Received request to resolve short URL: %s", short_url)
    
    try:
        # Forward the request to the url-shortener service
        response = requests.get(f"{settings.url_shortener_service}/r/{short_url}")
        logging.info("Forwarded request to url-shortener service for resolving: %s", response.url)
        response.raise_for_status()
        
        original_url = response.json().get('original_url')
        if original_url:
            logging.info("Resolved short URL to original URL: %s", original_url)
            return RedirectResponse(url=original_url)
        else:
            logging.error("Failed to retrieve original URL from url-shortener service")
            raise HTTPException(status_code=500, detail="Failed to get original URL from the shortener service")
    except requests.exceptions.RequestException as e:
        logging.error("Error resolving the short URL: %s", e)
        raise HTTPException(status_code=404, detail="Short URL not found") from e


@app.get("/")
async def index():
    logging.info("Health check on the URL shortener API")
    return "Your API service is running!"
