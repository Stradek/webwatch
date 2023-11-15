Configuration
=============

------------------------
Configuration file setup
------------------------
To configure webwatch, you need to create a configuration file.
Configuration file is a simple JSON file. It should be placed in the ``config/`` directory.

If no configuration file is specified, webwatch will try to load ``config/config.json`` file.
In this case, make sure that ``config/config.json`` file exists.
You can create it by copying example configuration file: ``config/example_config.json`` and renaming it to
``config.json``.

Windows:

.. code-block:: console

    > copy config/example_config.json config/config.json

Linux:

.. code-block:: bash

    $ cp config/example_config.json config/config.json

--------------------------
Configuration file options
--------------------------

.. autofunction:: watch_model.Watchlist

.. autofunction:: watch_model.WatchedItem

.. autofunction:: watch_model.WatchedItemFilter

