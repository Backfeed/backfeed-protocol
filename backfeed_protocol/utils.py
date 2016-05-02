
from sqlalchemy import engine_from_config

from models import initialize_sql
from models import DBSession
from models.contribution import Contribution
from models.contract import Contract
from models.evaluation import Evaluation
from models.user import User
from models import with_session
from contracts.dmag import DMagContract
from contracts.example import ExampleContract


def setup_database(
        settings={
            'sqlalchemy.url': 'sqlite:///:memory:',
        }):
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)


def reset_database():
    """delete all data from the database"""
    session = DBSession
    db_tables = [Evaluation, Contribution, User, Contract]
    for table in db_tables:
        session.query(table).delete()


@with_session
def get_contract(name='dmag', contract_id=1):
    """return the contract identified by name

    returns a Contract instance

    TODO: for now, this function returns a DMagContract()
    """
    if name == 'example':
        contract_class = ExampleContract
    elif name == 'dmag':
        contract_class = DMagContract
    else:
        raise ValueError('Unknown contract type: {name}'.format(name=name))
    contract = DBSession.query(contract_class).get(contract_id)
    if contract is None:
        contract = contract_class()
        DBSession.add(contract)
    return contract
