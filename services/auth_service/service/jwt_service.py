import os
import jwt

from service.model import JWTUser

JWT_SECRET = os.getenv("JWT_SECRET", default=None)
JWT_ALGO = os.getenv("JWT_ALGORITHM", default='HS256')

class JwtService:

    @staticmethod
    def generate_jwt_token(user: JWTUser) -> str:
        return jwt.encode(payload=user.model_dump(), key=JWT_SECRET, algorithm=JWT_ALGO)

