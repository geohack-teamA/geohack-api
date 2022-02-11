from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.api import router as api_router
from app.core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME


def get_app() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    # app.include_router(api_router, prefix=API_PREFIX)

    return app


app = get_app()
