from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from services.auth_service.api.routers import user

app = FastAPI()

app.include_router(user.app)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
