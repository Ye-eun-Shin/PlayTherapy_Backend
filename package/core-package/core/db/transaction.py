from contextlib import contextmanager


@contextmanager
def transaction_scope(session):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()