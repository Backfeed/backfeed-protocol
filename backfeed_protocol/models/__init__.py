from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def initialize_sql(engine):
    # TODO: set autocommit = False,
    # and implement some proper transaction handling
    from user import User  # NOQA
    from contract import Contract  # NOQA
    from evaluation import Evaluation  # NOQA
    from contribution import Contribution  # NOQA
    DBSession.configure(bind=engine, autoflush=True, autocommit=True)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
