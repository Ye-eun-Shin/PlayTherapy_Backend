import os
from dependency_injector import providers
from fastapi import FastAPI

from analyze.container import Container
from analyze.setting.config import settings
from analyze.route.monitor import router as monitor_router
from analyze.scheduler.script_batch import start_analyze

config = providers.Configuration()
container = Container()
container.config.from_yaml(f"./analyze/config-{os.getenv('PHASE','LOCAL')}.yaml")

container.wire(packages=["analyze.route", "analyze.scheduler"])

app = FastAPI(
    debug=True,
    title=settings.APP_TITLE,
    version=settings.VERSION,
)


def register_routers(app: FastAPI):
    app.include_router(
        monitor_router,
        prefix=f"/analyze/api/monitor",
    )


start_analyze()
register_routers(app)
