from fastapi import FastAPI

from app.database.connection import (
    Base,
    engine
)

from app.models.user import (
    User
)

from app.routers.auth import (
    router as auth_router
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="User Authentication Service",
    description="FastAPI authentication service with JWT authentication and refresh tokens",
    version="1.0.0"
)


app.include_router(
    auth_router,
    tags=["Authentication"]
)


@app.get("/")
def root():

    return {
        "message":
            "User Authentication Service"
    }


@app.get("/health")
def health_check():

    return {
        "status":
            "healthy"
    }