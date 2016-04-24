from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def initialize_sql(engine):
    from user import User  # NOQA
    from contract import Contract  # NOQA
    from evaluation import Evaluation  # NOQA
    from contribution import Contribution  # NOQA
    DBSession.configure(bind=engine, autoflush=True)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


def with_session(fn):
    """a decorator for functions that do database operations"""
    def go(*args, **kw):
        DBSession.begin(subtransactions=True)
        try:
            ret = fn(*args, **kw)
            DBSession.commit()
            return ret
        except:
            # DBSession.rollback()
            raise
    return go
