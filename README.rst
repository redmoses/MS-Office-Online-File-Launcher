Poom
====

Open document files from your local file system in the free Microsoft
Office Online version on your browser.

What?
-----

The app is primarily a dropbox client. When a document file is opened
using the app it uploads the file to your Dropbox and opens it from
there using Microsoft Office Online.

Technology
~~~~~~~~~~

-  Python 3
-  Python 2.7.8 (older version 0.0.2)
-  The superb `Dropbox
   API <https://www.dropbox.com/developers/core/docs/python>`__ for
   python.

How?
----

The app doesn't have any permission over your existing Dropbox files. So
when you open a document with the app it first uploads the file to its
own directory on your Dropbox and then open the file from there using
the Microsoft Office online edition.

File Syncing Feature
--------------------

Once you've edited the file in Dropbox the changes are going to be
temporarily saved there. The next time you open the same file using this
app it will show you the last modified version of the file, meaning if
the file was last modified on Dropbox it will open the Dropbox version
and sync your local file and vice versa.

Installation
------------

Latest version (Python 3)
~~~~~~~~~~~~~~~~~~~~~~~~~

For system installation

.. code:: bash

    sudo pip install poom

If Python 3 is not the default interpreter in your system then you must
install the package using pip3

.. code:: bash

    sudo pip3 install poom

For installing from github source

.. code:: bash

    git clone https://github.com/redmoses/poom.git
    cd poom
    # for python2 as the system's default python
    sudo python3 setup.py install
    # for python3 as the system's default python
    sudo python setup.py install

Installing version 0.0.2 (Python 2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For system installation

.. code:: bash

    sudo pip install poom=0.0.2

Usage
-----

After installing the app, use the following command to open document
files

.. code:: bash

    poom /path/to/office/document

