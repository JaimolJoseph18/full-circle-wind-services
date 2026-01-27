from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from functools import wraps
from backend.shared.database.engine import engine
from backend.shared.logger.logger import get_logger

logger = get_logger(__name__)

SessionFactory = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, future=True
)

Session = scoped_session(SessionFactory)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        logger.exception("Database transaction failed")
        raise
    finally:
        session.close()


def with_db_session(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        with session_scope() as session:
            return func(*args, **kwargs, session=session)

    return wrapped
