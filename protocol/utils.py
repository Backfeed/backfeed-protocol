def setup_database():
    from protocol.settings import database
    database.connect()
    from protocol.models.user import User
    from protocol.models.contribution import Contribution
    from protocol.models.evaluation import Evaluation
    database.create_tables([User, Contribution, Evaluation], safe=True)