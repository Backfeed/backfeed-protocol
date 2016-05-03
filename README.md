Backfeed Protocols  
[![Build Status](https://travis-ci.org/Backfeed/backfeed-protocol.svg?branch=master)](https://travis-ci.org/Backfeed/backfeed-protocol)
--------------------------------


This Python package contains 'standalone' implementations of the Backfeed protocols.

## Installation

You need pip installed

    sudo apt-get install python-pip

You can now either directly install from the github repository:

     pip install git+https://github.com/Backfeed/backfeed-protocol.git

or install from your local copy

    git clone https://github.com/Backfeed/backfeed-protocol.git
    cd backfeed-protocol
    pip install .

## Running the tests

You can run the tests in a sandboxed environment using tox:

    pip install tox

    git clone https://github.com/Backfeed/backfeed-protocol.git
    cd backfeed-protocol
    tox

or, if you just want to run the tests, without the syntax checks:

     python setup.py test

or, if you want to run individual tests:

    py.test path/to/your/testfile.py


##  Usage

Once you have the package installed, you can use it like this:

    python
    >>> # set up a database
    >>> # (with the default settings, this is a in-memory sqlite database)
    >>> from backfeed_protocol import utils
    >>> utils.setup_database()

    >>> # create a contract
    >>> contract = utils.get_contract(u'example')

    >>> # add two users
    >>> ann  = contract.create_user(tokens=10, reputation=10)
    >>> bonnie = contract.create_user(tokens=99, reputation=100)
    >>> ann.reputation
    10.0
    >>> ann.tokens
    10.0

    >>> # ann makes a contribution
    >>> contribution = contract.create_contribution(user=ann,contribution_type=u'article')
    >>> # In the Example contract, this will have cost Ann 1 token
    >>> ann.tokens
    9.0

    >>> # bonnie now evaluates the contribution of ann
    >>> evaluation = contract.create_evaluation(contribution=contribution, user=bonnie, value=1)
    >>> # bonnie pays a reputation fee to make the evaluation
    >>> bonnie.reputation
    99.90692517849118
    >>> # because bonnie represents the majority, ann will get a reward
    >>> ann.tokens
    54.45069613049415
    >>> ann.reputation
    14.545069613049415

## Contributing

See [../CONTRIBUTING.md](CONTRIBUTING.md)
