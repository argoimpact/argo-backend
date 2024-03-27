from pydantic_settings import BaseSettings, SettingsConfigDict
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Constants
    clerk_api_endpoint: str = "https://api.clerk.com/v1"
    redis_host: str = "redis"

    # clerk
    jwt_algorithm: str = "HS256"

    ## OpenAI
    embedding_model_small: str = "text-embedding-3-small"
    embedding_model_large: str = "text-embedding-3-large"
    embedding_model_ada: str = "text-embedding-ada-002"

    # Env variables
    # (uppsercase of same string, if it an actual environment variableis picked up by pydantic and used as default value)
    # Pinecone
    pinecone_index_host: str  # TODO: add this to env variables in github

    # API Keys
    openai_api_key: str
    clerk_secret_key: str
    clerk_api_key: str
    pinecone_api_key: str


app_config = AppConfig()
