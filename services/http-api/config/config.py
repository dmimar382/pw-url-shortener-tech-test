from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    mongo_url: str
    base_url: str


# Initialize the settings object
settings = Settings()
