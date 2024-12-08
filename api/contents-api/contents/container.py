from dependency_injector import containers, providers

from core.repository.user import UserRepository
from core.repository.case import CaseRepository
from core.repository.session import SessionRepository
from core.db.connection import ConnectionManager
from core.service.security import SecurityService
from object.repository.video import VideoRepository
from object.repository.script import ScriptRepository
from object.repository.analyze_report import AnalyzeReportRepository
from object.storage.client import ClientManager
from contents.service.case import CaseService
from contents.service.session import SessionService
from contents.service.video import VideoManagerService
from contents.service.script import ScriptManagerService
from contents.service.analyze_report import AnalyzeReportManagerService


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

    # core repositories
    case_repository = providers.Singleton(
        CaseRepository, connection_manager=connection_manager
    )

    user_repository = providers.Singleton(
        UserRepository, connection_manager=connection_manager
    )

    session_repository = providers.Singleton(
        SessionRepository, connection_manager=connection_manager
    )
    # object services
    client_manager = providers.Singleton(
        ClientManager,
        aws_access_key_id=config.aws.access_key,
        aws_secret_access_key=config.aws.secret_key,
        region_name=config.aws.region,
    )

    # object repositories
    video_repository = providers.Singleton(
        VideoRepository, bucket=config.aws.bucket, client_manager=client_manager
    )

    script_repository = providers.Singleton(
        ScriptRepository, bucket=config.aws.bucket, client_manager=client_manager
    )

    analyze_report_repository = providers.Singleton(
        AnalyzeReportRepository, bucket=config.aws.bucket, client_manager=client_manager
    )

    # domain services
    case_service = providers.Singleton(
        CaseService,
        case_repository=case_repository,
        security_service=security_service,
        connection_manager=connection_manager,
    )

    session_service = providers.Singleton(
        SessionService,
        session_repository=session_repository,
        case_repository=case_repository,
        security_service=security_service,
        connection_manager=connection_manager,
    )

    video_manager_service = providers.Singleton(
        VideoManagerService,
        video_repository=video_repository,
        session_repository=session_repository,
        case_repository=case_repository,
        connection_manager=connection_manager,
    )

    script_manager_service = providers.Singleton(
        ScriptManagerService,
        script_repository=script_repository,
        session_repository=session_repository,
        case_repository=case_repository,
        connection_manager=connection_manager,
    )

    analyze_report_manager_service = providers.Singleton(
        AnalyzeReportManagerService,
        analyze_report_repository=analyze_report_repository,
        session_repository=session_repository,
        case_repository=case_repository,
    )
