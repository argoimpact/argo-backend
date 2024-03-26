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

    ## OpenAI
    embedding_model_small: str = "text-embedding-3-small"
    embedding_model_large: str = "text-embedding-3-large"
    embedding_model_ada: str = "text-embedding-ada-002"

    # embedding model used for each pinecone index
    embeddings_config: dict[str, str] = {
        "index1": "embedding_model1",
        "index2": "embedding_model2",
    }

    # clerk
    jwt_algorithm: str = "HS256"

    # API Keys
    openai_api_key: str
    clerk_secret_key: str
    clerk_api_key: str
    pinecone_api_key: str


app_config = AppConfig()
