
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. 

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
----------------------

Report bugs at <https://github.com/Backfeed/backfeed-protocol/issues>.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
----------------------

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
----------------------

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
----------------------

The Backfeed Protocol could always use more documentation, whether as part of the official Backfeed Protocol  docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
----------------------

The best way to send feedback is to file an issue at <https://github.com/Backfeed/backfeed-protocol/issues>

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.


Get Started!
------------

Ready to contribute? Here's how to set up `backfeed-protocol` for
local development.

1. Fork the `backfeed-protocol` repo on GitHub on <https://github.com/Backfeed/backfeed-protocol/fork>. 

    Or, if you have write access to the Backfeed repository, you can directly pass to step 2 and clone the Backfeed/backfeed-protocol.git repository directly.

2. Clone your fork locally::

    ```
    $ git clone git@github.com:your_name_here/backfeed-protocol.git
    ```

3. Create a branch for local development::

    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

Now you can make your changes locally.

4. When you're done making changes, check that your changes pass style and unit
   tests, including testing other Python versions with tox::

    ```
    $ tox
    ```

To get tox, just pip install it.

5. Commit your changes and push your branch to GitHub::

    ```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

6. Submit a pull request through the GitHub website.


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. Run the ``tox`` command and make sure that the tests pass for all supported Python versions.


Tips
----

To run a subset of tests::

    $ py.test tests/test_sanity.py