def setup_database(sqlite_file=':memory:'):
    from settings import database
    from models.user import User
    from models.contribution import Contribution
    from models.evaluation import Evaluation

    database.init(sqlite_file)
    database.connect()
    database.create_tables([User, Contribution, Evaluation], safe=True)


def reset_database():
    """delete all data from the database"""
    from .models.contribution import Contribution
    from .models.evaluation import Evaluation
    from .models.user import User

    db_tables = [Contribution, Evaluation, User]
    for table in db_tables:
        table.delete().execute()
