from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import user_router, course_assignment_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(course_assignment_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
