

def get_contract(name=None, sqllite_file=None):
    """return the contract identified by name

    returns a Contract instance

    TODO: for now, this functino returns a DMagContract()
    """
    from contracts.dmag import DMagContract
    return DMagContract()
