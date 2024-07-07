from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import dotenv

dotenv.load_dotenv()

class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    app_name: str ="HNG APP"

    SECRET_KEY: str
    ALGORITHM: str
    APP_STATE: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool = True

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='allow' # or 'allow' if you want to allow extra fields
    )


class ProductionSettings(Settings):
    database_url: str =f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@localhost/hng_prod_db"
    DEBUG: bool = False

class TestSettings(Settings):
    database_url: str =f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@localhost/hng_test_db"


def get_settings():
    settings = Settings()
    app_state = os.getenv("APP_STATE")
    
    if app_state == "testing":
        settings = TestSettings()
    elif app_state == "production":
        settings = ProductionSettings
    return settings