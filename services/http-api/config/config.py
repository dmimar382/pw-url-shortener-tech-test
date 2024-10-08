from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    grpc_host: str
    grpc_port: int
 

# Initialize the settings object
settings = Settings()
