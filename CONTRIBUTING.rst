#################
Contributor guide
#################

This document provides guidelines for people who want to contribute to the
project.


**************
Create tickets
**************

Please use the `bugtracker`_ **before** starting some work:

* check if the bug or feature request has already been filed. It may have been
  answered too!
* else create a new ticket.
* if you plan to contribute, tell us, so that we are given an opportunity to
  give feedback as soon as possible.
* Then, in your commit messages, reference the ticket with some
  ``refs #TICKET-ID`` syntax.


***************
Fork and branch
***************

* Work in forks and branches, use git-flow.

* Prefix your branch with the ticket ID corresponding to the issue. As an
  example, if you are working on ticket #23 which is about contribute
  documentation, name your branch like ``feature/23-contribute-doc`` using
  ``git flow feature start 23-contribute-doc``.


*******************************
Setup a development environment
*******************************

System requirements:

* `Python`_ version 2.7, available as ``python`` command.
  
  .. note::

     You may use `Virtualenv`_ to make sure the active ``python`` is the right
     one.

* make and wget to use the provided `Makefile`.

* `Docker`_ is the suggested tool to setup and run Odoo service. Continuous
  integration uses Docker. See ``docker-compose.yml`` and ``.travis.yml``.

  Docker is used to serve Odoo at ``http://localhost:8069``, with user
  ``admin``, password ``admin`` and database ``test``. These values will be
  used within `odooselenium`'s own tests.

Execute:

.. code-block:: sh

   git clone git@github.com/meta-it/odooselenium.git
   cd odooselenium/
   make test

If you cannot execute the Makefile, read it and adapt the few commands it
contains to your needs.


************
The Makefile
************

A `Makefile` is provided to ease development. Use it to:

* run tests: ``make test``

The `Makefile` is intended to be a live reference for the development
environment.


**************
Test and build
**************

Use `the Makefile`_.


.. rubric:: References

.. target-notes::

.. _`bugtracker`: 
   https://github.com/meta-it/odooselenium/issues
.. _`Python`: https://www.python.org
.. _`Virtualenv`: https://virtualenv.pypa.io/en/latest/
.. _`Docker`: https://www.docker.com/
