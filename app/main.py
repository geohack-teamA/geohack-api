from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.api import router as api_router
from app.core.config import DEBUG, PROJECT_NAME


def get_app() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG)

    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://naradeha.netlify.app", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_app()
