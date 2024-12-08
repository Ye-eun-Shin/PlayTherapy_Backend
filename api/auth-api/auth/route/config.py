from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from auth.service.config import ConfigService
from auth.container import Container

router = APIRouter()


@router.get("/config", tags=["config"])
@inject
async def get_config(
    config_service: ConfigService = Depends(Provide[Container.config_service]),
):
    config = await config_service.get()
    return config
