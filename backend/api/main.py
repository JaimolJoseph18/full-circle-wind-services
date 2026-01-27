from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import data_monitering
from backend.shared.logger.logger import get_logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


logger = get_logger(__name__)


def get_api_app() -> FastAPI:
    api = FastAPI(title="Data Monitoring API", root_path='/api')
    api.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    api.include_router(
        data_monitering.router,
        tags=["Data Monitoring"],
        prefix="/data-monitoring"
    )
    return api


def get_app(api_app: FastAPI) -> FastAPI:
    """
    Construct main fastapi application and
    mount api application on path /api
    """
    logger.info("Starting Data Monitoring API")

    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.mount("/api", app=api_app)
    return app


api_app: FastAPI = get_api_app()
app: FastAPI = get_app(api_app)
