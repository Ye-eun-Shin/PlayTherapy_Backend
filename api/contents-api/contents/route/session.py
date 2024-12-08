from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide

from contents.dto.session import SessionRequest
from contents.service.session import SessionService
from contents.container import Container
from core.service.security import SecurityService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/api/signin")


@router.get(
    "/case/{case_id}/session/total-num",
    tags=["session"],
)
@inject
async def get_page_num(
    case_id: int,
    keyword: str = None,
    token: str = Depends(oauth2_scheme),
    session_service: SessionService = Depends(Provide[Container.session_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    page_num = await session_service.get_page_num(
        case_id=case_id, user_id=payload.get("user_id"), keyword=keyword
    )
    return page_num


@router.get(
    "/case/{case_id}/session",
    tags=["session"],
)
@inject
async def get_session_list(
    case_id: int,
    skip: int = None,
    limit: int = None,
    keyword: str = None,
    token: str = Depends(oauth2_scheme),
    session_service: SessionService = Depends(Provide[Container.session_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    session_list = await session_service.get_session_list(
        case_id=case_id,
        skip=skip,
        limit=limit,
        user_id=payload.get("user_id"),
        keyword=keyword,
    )
    return session_list


# 특정 사례의 세션 가져오는 API
@router.get(
    "/case/{case_id}/session/{session_id}",
    tags=["session"],
)
@inject
async def get_session(
    case_id: int,
    session_id: int,
    token: str = Depends(oauth2_scheme),
    session_service: SessionService = Depends(Provide[Container.session_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    session = await session_service.get(
        case_id=case_id, session_id=session_id, user_id=payload.get("user_id")
    )
    return session


@router.post("/case/{case_id}/session", tags=["session"])
@inject
async def create_session(
    case_id: int,
    data: SessionRequest,
    token: str = Depends(oauth2_scheme),
    session_service: SessionService = Depends(Provide[Container.session_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    session = await session_service.add(
        case_id=case_id, user_id=payload.get("user_id"), data=data
    )
    return session


@router.put("/case/{case_id}/session/{session_id}", tags=["session"])
@inject
async def update_session(
    case_id: int,
    data: SessionRequest,
    session_id: int,
    token: str = Depends(oauth2_scheme),
    session_service: SessionService = Depends(Provide[Container.session_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    session = await session_service.update(
        case_id=case_id,
        session_id=session_id,
        user_id=payload.get("user_id"),
        data=data,
    )
    return session


@router.delete("/case/{case_id}/session/{session_id}", tags=["session"])
@inject
async def delete_session(
    case_id: int,
    session_id: int,
    token: str = Depends(oauth2_scheme),
    session_service: SessionService = Depends(Provide[Container.session_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    result = await session_service.delete(
        case_id=case_id, session_id=session_id, user_id=payload.get("user_id")
    )
    return result
