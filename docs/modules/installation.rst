Installation
============

Requirements
------------
- Python 3
- SQLite
- Django
- social-auth-app-django
- Sphinx
    To build documentation

Development
-----------
Django comes with its own builtin development server.

#. Install Python 3 and pip

   - You can get the latest version of Python 3 from python.org_

   - Instruction for installing pip can be found in the `pip documentation`_

   .. _python.org: https://www.python.org/downloads/
   .. _pip documentation:  https://pip.pypa.io/en/stable/installing/

#. Setup a python virtualenv

    #. Install virtualenv
        .. code-block:: shell

            pip install virtualenv

    #. Setup a new virtualenv

        Replace $ENVPATH with the path where you want to
        store your virtualenv files.

        .. code-block:: shell

            mkdir $PATHTOENV    # make virtualenv directory
            virtualenv $PATHTOENV/helpdesk   # create a new virtualenv
            cd $PATHTOENV/helpdesk    # move into virtualenv directory
            source bin/activate       # activate the new virtualenv

#. Install Dependencies

    .. code-block:: shell

        pip install -r requirements.txt

#. Download Source Code

   - With Git

   .. code-block:: shell

        git clone https://gitlab.com/winstc/helpdesk.git

#. Configure Credentials

   *credentials.py* is used to configure secrets for
   Google OAuth2 and the email server that is used to send
   users emails.

   - Google OAuth2

        Helpdesk can use *Google OAuth2* to authenticate users.
        Please refer to :doc:`oauth` for help configuring this.

   - Email Server

        In order for helpdesk to send email it will need a valid
        email server configured in *credentials.py*. Please refer to
        :doc:`email` for help configuring this.


#. Migrate Database

    .. code-block:: shell

        cd helpdes/helpdesk
        python3 manage.py makemigrations
        python3 manage.py migrate

#. Run Development Server

    With virtualenv activated

    .. code-block:: shell

        cd helpdesk/helpdesk
        python3 manage.py runserver 8000

     Navigate to 127.0.0.1:8000 in your browser


Production
----------

Helpdesk can be deployed in a production environment using mod_wsgi
and Apache.

