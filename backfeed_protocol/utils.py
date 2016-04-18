def setup_database(sqlite_file=':memory:'):
    from settings import database
    from models.user import User
    from models.contribution import Contribution
    from models.evaluation import Evaluation

    if database.database != sqlite_file:
        database.init(sqlite_file)
    database.connect()
    database.create_tables([User, Contribution, Evaluation], safe=True)


def init_database(sqlite_file):
    from settings import database
    if database.database != sqlite_file:
        database.init(sqlite_file)
    return database


def reset_database():
    """delete all data from the database"""
    from .models.contribution import Contribution
    from .models.evaluation import Evaluation
    from .models.user import User

    db_tables = [Contribution, Evaluation, User]
    for table in db_tables:
        table.delete().execute()
