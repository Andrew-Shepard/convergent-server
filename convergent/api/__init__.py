import logging
from fastapi import FastAPI
from convergent.settings import Settings
from convergent.external.reporter import LogReporter
from convergent.api.routes import root as root_router
from convergent.db.dependencies import init_db


def create_app(settings: Settings):
    app = FastAPI()
    app.reporter = LogReporter()
    app.include_router(root_router)

    @app.on_event("startup")
    async def _startup():
        init_logger(settings.log_level)
        await init_db(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_database,
        )

    @app.on_event("shutdown")
    async def _shutdown():
        """
        Clean up before closing the application
        """
        pass

    return app


def init_logger(log_level):
    logging.basicConfig(
        format="%(asctime)s|%(name)s|%(levelname)-5.5s|%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    logger = logging.getLogger()
    logger.setLevel(log_level)
