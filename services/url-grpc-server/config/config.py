from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    mongo_url: str
    grpc_host: str
    grpc_port: int


# Initialize the settings object
settings = Settings()
