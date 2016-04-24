

def setup_database(settings={
        'sqlalchemy.url': 'sqlite:///:memory:',
    }):
    from models import initialize_sql
    from sqlalchemy import engine_from_config
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)


def reset_database():
    """delete all data from the database"""
    from .models.contribution import Contribution
    from models.contract import Contract
    from .models.evaluation import Evaluation
    from .models.user import User
    from .models import DBSession

    session = DBSession
    db_tables = [Contract, Contribution, Evaluation, User]
    for table in db_tables:
        session.query(table).delete()


def get_contract(name=None, contract_id=1):
    """return the contract identified by name

    returns a Contract instance

    TODO: for now, this functino returns a DMagContract()
    """
    from contracts.dmag import DMagContract
    from .models import DBSession

    contract = DBSession.query(DMagContract).get(contract_id)
    if contract is None:
        contract = DMagContract()
        DBSession.add(contract)
        DBSession.flush()
    return contract
