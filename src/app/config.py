from pydantic import BaseSettings, SecretStr


class PostgresPoolConfig(BaseSettings):
    """Конфигурация для хранения данных коннекта к PostgreSQL."""

    db_user: str
    db_password: SecretStr
    db_host: str
    db_name: str
    db_port: str

    min_size_pull: int
    max_size_pull: int

    class Config:
        env_file = '.env'
