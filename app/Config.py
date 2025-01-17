from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname   :str
    database_name       :str
    secret_key          :str
    password            :str
    algorithm           :str
    database_username   :str
    token_expiration    :int

    class Config:
        env_file = ".env"

settings = Settings()