from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide

from contents.dto.case import CaseRequest
from contents.service.case import CaseService
from contents.container import Container
from core.service.security import SecurityService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/api/signin")


@router.get("/total-num", tags=["case"])
@inject
async def get_page_num(
    keyword: str = None,
    token: str = Depends(oauth2_scheme),
    case_service: CaseService = Depends(Provide[Container.case_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    page_num = await case_service.get_page_num(
        user_id=payload.get("user_id"), keyword=keyword
    )
    return page_num


@router.get("", tags=["case"])
@inject
async def get_case_list(
    skip: int = None,
    limit: int = None,
    keyword: str = None,
    token: str = Depends(oauth2_scheme),
    case_service: CaseService = Depends(Provide[Container.case_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    case_list = await case_service.get_case_list(
        skip=skip, limit=limit, user_id=payload.get("user_id"), keyword=keyword
    )
    return case_list


@router.get("/{case_id}", tags=["case"])
@inject
async def get_case(
    case_id: int,
    token: str = Depends(oauth2_scheme),
    case_service: CaseService = Depends(Provide[Container.case_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    case = await case_service.get(case_id=case_id, user_id=payload.get("user_id"))
    return case


@router.post("", tags=["case"])
@inject
async def create_case(
    case: CaseRequest,
    token: str = Depends(oauth2_scheme),
    case_service: CaseService = Depends(Provide[Container.case_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    case = await case_service.add(payload.get("user_id"), case)
    return case


@router.put("/{case_id}", tags=["case"])
@inject
async def update_case(
    case_id: int,
    case: CaseRequest,
    token: str = Depends(oauth2_scheme),
    case_service: CaseService = Depends(Provide[Container.case_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    case = await case_service.update(payload.get("user_id"), case_id, case)
    return case


@router.delete("/{case_id}", tags=["case"])
@inject
async def delete_case(
    case_id: int,
    token: str = Depends(oauth2_scheme),
    case_service: CaseService = Depends(Provide[Container.case_service]),
    security_service: SecurityService = Depends(Provide[Container.security_service]),
):
    payload = security_service.verify_token(token)
    result = await case_service.delete(payload.get("user_id"), case_id)
    return result
