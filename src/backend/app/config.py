from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "AI Finance Hub API"
    environment: str = "dev"


settings = Settings()
