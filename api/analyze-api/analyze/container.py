from dependency_injector import containers, providers

from analyze.repository.observation import ObservationRepository
from analyze.service.langflow_service import LangflowService
from analyze.service.analyze import AnalyzeService
from analyze.service.observation import ObservationService

from core.repository.session import SessionRepository
from core.db.connection import ConnectionManager
from core.service.security import SecurityService
from object.storage.client import ClientManager
from object.repository.script import ScriptRepository
from object.repository.analyze_report import AnalyzeReportRepository
from object.service.script import ScriptService
from object.service.analyze_report import AnalyzeReportService


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
    session_repository = providers.Singleton(
        SessionRepository, connection_manager=connection_manager
    )

    # object repositories
    client_manager = providers.Singleton(
        ClientManager,
        aws_access_key_id=config.aws.access_key,
        aws_secret_access_key=config.aws.secret_key,
        region_name=config.aws.region,
    )
    script_repository = providers.Singleton(
        ScriptRepository,
        bucket=config.aws.bucket,
        client_manager=client_manager,
    )
    analyze_report_repository = providers.Singleton(
        AnalyzeReportRepository,
        bucket=config.aws.bucket,
        client_manager=client_manager,
    )

    # object services
    script_service = providers.Singleton(
        ScriptService,
        script_repository=script_repository,
    )
    analyze_report_service = providers.Singleton(
        AnalyzeReportService,
        analyze_report_repository=analyze_report_repository,
    )

    # domain repository
    observation_repository = providers.Singleton(
        ObservationRepository, connection_manager=connection_manager
    )

    # domain services
    observation_service = providers.Singleton(
        ObservationService,
        observation_repository=observation_repository,
    )

    langflow_service = providers.Singleton(
        LangflowService,
        langflow_host=config.langflow.host,
        langflow_token=config.langflow.token,
        flow_id=config.langflow.flow_id,
    )

    analyze_service = providers.Singleton(
        AnalyzeService,
        connection_manager=connection_manager,
        script_service=script_service,
        analyze_report_service=analyze_report_service,
        session_repository=session_repository,
        langflow_service=langflow_service,
        observation_service=observation_service,
    )
