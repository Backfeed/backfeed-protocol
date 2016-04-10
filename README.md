Backfeed Protocols 
--------------------------------

This Python package contains 'standalone' implementations of the Backfeed protocols.

## Installation

You need setuptools installed for this to work

    git clone https://github.com/Backfeed/backfeed-protocol.git
    cd backfeed-protocol
    python setup.py install

For development:

    python setup.py develop

## Running tests

    python setup.py test


# Usage

Once you have the package installed, you can use it like this:

    python
    >>> # (with the default settings, this is a in-memory sqllite database)
    >>> from protocol import utils
    >>> utils.setup_database()
    >>> from protocol.contracts.dmag import DMagContract
    >>> # create a contract instance
    >>> contract = DMagContract()
    >>> # add two users
    >>> ann  = contract.add_user(tokens=10, reputation=10) 
    >>> bonnie = contract.add_user(tokens=99, reputation=100)
    >>> ann.reputation
    10
    >>> ann.tokens
    10
    >>> # ann makes a contribution
    >>> contribution = contract.add_contribution(user=ann)
    >>> # In the DmagContract, this will have cost Ann 1 token
    >>> ann.tokens
    9
    >>> # bonnie now evaluates the contribution of ann
    >>> evaluation = contract.add_evaluation(contribution=contribution, user=bonnie, value=1)
    >>> # bonnie pays a reputation fee to make the evaluation
    >>> bonnie.reputation
    99.90692517849118
    >>> # because bonnie represents the majority, ann will get a reward
    >>> ann.tokens
    54.45069613049415
    >>> ann.reputation
    14.545069613049415

