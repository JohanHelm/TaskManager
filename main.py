import uvicorn
from fastapi import FastAPI

from app.api.endpoints.tasks import tasks_router
from app.settings.initial_settings import AppParams
from app.settings.logging_settings import configure_logger
from app.utils import create_fake_db, create_necessary_catalogs

app = FastAPI()


app.include_router(tasks_router)


if __name__ == "__main__":
    create_necessary_catalogs()
    create_fake_db()
    logger = configure_logger(__name__)
    logger.info(f"Starting app with {AppParams}")

    uvicorn.run(AppParams.app,
                host=AppParams.host,
                port=AppParams.port,
                reload=AppParams.reload,
                workers=AppParams.workers,
                )
