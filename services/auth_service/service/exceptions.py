from fastapi import HTTPException


class YandexDataError(HTTPException):
    def __init__(self, details):
        super().__init__(
            400,
            details,
        )
