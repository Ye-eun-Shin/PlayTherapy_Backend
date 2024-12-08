from abc import ABC
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import registry
from sqlalchemy.orm import declarative_base
from core.db.common_declarative_base import Base

class ConnectionManager(ABC):
    def __init__(self, db_url: str, pool_recycle: int):
        self.engine = create_engine(db_url, pool_recycle=pool_recycle)
        self.mapper_registry = registry()
        self.mapper_registry.metadata.create_all(self.engine)
        Base.metadata.create_all(self.engine)

    def make_session(self) -> Session:
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)()

    @staticmethod
    def manage_db_session(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            db_session = kwargs.get("db_session")
            if db_session is None:
                db_session = self.connection_manager.make_session()
                kwargs["db_session"] = db_session
                should_close = True
            else:
                should_close = False

            result = func(self, *args, **kwargs)

            if should_close:
                db_session.close()

            return result

        return wrapper

    @staticmethod
    def manage_db_session_with_transaction(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            db_session = kwargs.get("db_session")
            if db_session is None:
                db_session = self.connection_manager.make_session()
                kwargs["db_session"] = db_session
                should_commit_and_close = True
            else:
                should_commit_and_close = False

            result = func(self, *args, **kwargs)

            if should_commit_and_close:
                if result:
                    db_session.commit()
                db_session.close()

            return result

        return wrapper
