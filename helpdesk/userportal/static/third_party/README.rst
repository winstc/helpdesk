Helpdesk requires several third party libraries to function properly. Without them the site will run but styling and scripts
will not work.

To reduce clutter these files are not included in the git repository. A script is included to easily download them from
unpkg.com. To use this script, from a console with the python virtualenv activated, run:

    python3 helpdesk/manage.py fetch_third_party_libs

This will automatically download all needed files according to third-party-libs.json and place them in the correct folders.

These actions can be easily undone with the -c or --clean flag. All third party files will be deleted.

    python3 helpdesk/manage.py fetch_third_party_libs -c