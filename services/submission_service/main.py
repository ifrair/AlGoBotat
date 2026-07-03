import uvicorn

from api.app import app  # noqa


def main():
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        reload=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
