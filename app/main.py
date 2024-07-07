from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from .api import user, org, auth
from .database import engine, Base
from .config import get_settings, Settings
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from .utils import format_validation_errors

def create_app():
    app = FastAPI()

    # Setup database
    Base.metadata.create_all(bind=engine)

    # Include routers
    app.include_router(user.router)
    app.include_router(org.router)
    app.include_router(auth.router)

    settings = get_settings()
    @app.get("/")
    def root():
        return {"message": f"Welcome to {settings.app_name}"}
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(format_validation_errors(exc), status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    return app

# Create an app instance
app = create_app()
client = TestClient(app)