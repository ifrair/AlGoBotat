import os
import jwt

from service.model import JWTUser

JWT_KEY = os.getenv("JWT_KEY", default=None)
JWT_ALGO = "HS256"


class JwtService:
    @staticmethod
    def generate_jwt_token(user: JWTUser) -> str:
        return jwt.encode(payload=user.model_dump(), key=JWT_KEY, algorithm=JWT_ALGO)
