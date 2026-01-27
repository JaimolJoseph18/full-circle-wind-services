import asyncio
import traceback
from fastapi import FastAPI
from backend.shared.logger.logger import get_logger
from .monitering_engine import start_data_moniterig_engine

logger = get_logger(__name__)


def get_app() -> FastAPI:
    """
    Construct main fastapi application
    """
    logger.info("Starting Data Monitoring Engine")
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

    @app.on_event("startup")
    async def startup_event():
        """
        Instantiate data monitoring and run it
        as long running asyncio tasks.
        """
        logger.info("start main app!")
        try:
            app.state.data_monitering_task = asyncio.create_task(
                start_data_moniterig_engine()
            )
            logger.info("intializing data monitering engine")
        except Exception as e:
            logger.exception("Exception detected", e)
            traceback.print_exc()
            exit()

    @app.on_event("shutdown")
    def stop():
        pass

    return app


app: FastAPI = get_app()
