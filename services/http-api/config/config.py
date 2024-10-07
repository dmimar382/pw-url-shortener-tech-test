from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    url_shortener_service: str
 

# Initialize the settings object
settings = Settings()
