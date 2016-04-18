

def get_contract(name=None):
    """return the contract identified by name

    returns a Contract instance

    TODO: for now, this functino returns a DMagContract()
    """
    from contracts.dmag import DMagContract

    try:
        contract = DMagContract().get(id=1)
    except:
        contract = DMagContract()
        contract.save()
    return contract
