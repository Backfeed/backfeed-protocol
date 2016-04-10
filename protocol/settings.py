from peewee import SqliteDatabase


database = SqliteDatabase(':memory:')


def initialize_database():

    from .models.user import User
    from .models.evaluation import Evaluation
    from .models.contribution import Contribution
    db_tables = [User, Evaluation, Contribution]
    database.connect()
    database.create_tables(db_tables, safe=True)
