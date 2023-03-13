import logging
from fastapi import FastAPI
from convergent.settings import Settings
from convergent.external.reporter import logger
from convergent.api.routes import root as root_router
from convergent.db.dependencies import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


def create_app(settings: Settings):
    app = FastAPI()
    app.reporter = logger
    app.include_router(root_router)
    
    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

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
