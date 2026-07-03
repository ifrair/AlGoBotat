from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import auth

app = FastAPI()

app.include_router(auth.app)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
