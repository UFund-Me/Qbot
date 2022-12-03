from pydantic import BaseSettings


class APISettings(BaseSettings):
    max_wait_time_count: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
