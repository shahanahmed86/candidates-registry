from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    ENVIRONMENT: str
    BCRYPT_SALT: str
    JWT_SECRET: str
    JWT_EXPIRY: str
    JWT_ALGORITHM: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_ROOT_USERNAME: str
    DB_ROOT_PASSWORD: str
    SENTRY_DSN: str
    BROKER: str

    """
    SettingsConfigDict can be imported from pydantic_settings package

    use below code to load secrets from a .env
    model_config = SettingsConfigDict(env_file=".env")
    """


configs = Configs()
