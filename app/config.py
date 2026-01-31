import os
from dataclasses import dataclass


@dataclass
class Settings:
    openai_api_key: str
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_db: str
    chroma_dir: str
    policy_dir: str


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        mysql_host=os.getenv("MYSQL_HOST", "localhost"),
        mysql_port=int(os.getenv("MYSQL_PORT", "3306")),
        mysql_user=os.getenv("MYSQL_USER", ""),
        mysql_password=os.getenv("MYSQL_PASSWORD", ""),
        mysql_db=os.getenv("MYSQL_DB", "structured_DB"),
        chroma_dir=os.getenv("CHROMA_DIR", "./chroma_db"),
        policy_dir=os.getenv("POLICY_DIR", "./data/policies"),
    )
