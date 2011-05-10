Developing Freemix
==================

Setup
-----

UNIX-like systems, including Mac OS X and Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Requires::

    * Python 2.6.x
    * virtualenv 1.4.3+ (easy_install2.6 virtualenv)

To build::

    $ virtualenv --no-site-packages --distribute recollection
    $ cd recollection
    $ source bin/activate
    $ pip install -e hg+http://foundry.zepheira.com/hg/recollection#egg=recollection
    $ pip install -r src/recollection/requirements/develop.txt

To create the database::

    $ cd src/freemix/freemix/
    $ manage.py syncdb --noinput
    $ manage.py migrate
    $ manage.py createsuperuser

To run the server on port 8000::

    $ manage.py runserver_plus

The following should be run at a regular interval::

    $ manage.py send_mail



Windows
^^^^^^^

Download and run the latest Python 2.6 installer from
    http://www.python.org/download/

Download and run the latest setuptools installer from
    http://pypi.python.org/pypi/setuptools#files

Download and run the latest Mercurial and TortoiseHg installer from
    http://tortoisehg.bitbucket.org/download/index.html

Download and run the latest MinGW installer from
    http://sourceforge.net/projects/mingw/files/

The most user-friendly download is labelled "Automated MinGW Installer".
Make sure to select both g++ and MinGW Make from the options.

Some packages will require C/C++ compilation, which is what MinGW is for.
In your Windows home directory, create a file called pydistutils.cfg and
save it with the contents::

    [build]
    compiler=mingw32

Set PYTHON_PATH to C:\Python26\ (or wherever you choose to install it),
and add ";%PYTHON_PATH%\Scripts\;C:\MinGW\bin\" to the Windows PATH
variable (again depending on where you installed MinGW).

You should now be able to open up the DOS Prompt and run gcc and
easy_install from the command line (getting normal errors about arguments
as opposed to unknown commands).

At the prompt, run::

    $ easy_install virtualenv
    $ virtualenv --no-site-packages --distribute recollection
    $ cd recollection/Scripts
    $ activate.bat
    $ cd ..
    $ pip install -e hg+http://foundry.zepheira.com/hg/recollection#egg=recollection
    $ pip install -r src/recollection/requirements/develop.txt


Tagging a Release
-----------------

The freemix version number depends on the BASE_VERSION tuple set in *freemix/__init__.py*.  If the version specified in BASE_VERSION corresponds to a tag of the form X.Y.Z on the current mercurial revision, or if there is a VERSION.py file in the root freemix module, the version returned will be X.Y.Z.  Otherwise, the version will by X.Y.ZdevR, where R is the current mercurial revision.

A freemix release is tagged at X.Y.Z as follows::

    $ cd /path/to/hg/checkout/freemix
    $ vi freemix/__init__.py # Validate that BASE_VERSION = (X,Y,Z,)
    $ hg commit -m "upping version number to X.Y.Z" # Only if the version needed changing
    $ hg tag X.Y.Z
    $ vi freemix/__init__.py # Update BASE_VERSION to the next expected version number
    $ hg push http://foundry.zepheira.com/hg/freemix

