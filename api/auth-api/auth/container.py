import os

from configparser import ConfigParser

from dependency_injector import containers, providers

from core.repository.org import OrgRepository
from core.repository.user import UserRepository, UserTypeRepository
from core.repository.whitelist import WhitelistRepository
from auth.service.auth import AuthService
from auth.service.config import ConfigService
from auth.service.user import UserService
from core.db.connection import ConnectionManager
from core.service.security import SecurityService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["."])

    config = providers.Configuration()

    # core services
    connection_manager = providers.Singleton(
        ConnectionManager,
        db_url=config.mysql.db_url,
        pool_recycle=config.mysql.pool_recycle,
    )

    security_service = providers.Singleton(
        SecurityService,
        secret_key=config.security.secret_key,
        algorithm=config.security.algorithm,
        expires_delta=config.security.expires_delta,
    )

    # repositories
    org_repository = providers.Singleton(
        OrgRepository, connection_manager=connection_manager
    )

    user_repository = providers.Singleton(
        UserRepository, connection_manager=connection_manager
    )

    user_type_repository = providers.Singleton(
        UserTypeRepository, connection_manager=connection_manager
    )

    whitelist_repository = providers.Singleton(
        WhitelistRepository, connection_manager=connection_manager
    )


    # domain services
    user_service = providers.Singleton(
        UserService,
        user_repository=user_repository,
        whitelist_repository=whitelist_repository,
        org_repository=org_repository,
        security_service=security_service,
        connection_manager=connection_manager,
    )

    auth_service = providers.Singleton(
        AuthService,
        user_service=user_service,
        security_service=security_service,
    )

    config_service = providers.Singleton(
        ConfigService,
        user_type_repository=user_type_repository,
        org_repository=org_repository,
    )
