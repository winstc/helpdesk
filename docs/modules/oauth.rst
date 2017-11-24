Google OAuth2
=============

Helpdesk can use Google OAuth2 to authenticate users.
This is helpful if your organization uses Google Apps
because users can sign in using their existing Google
account.

API Keys
--------

For the feature to work you will need a valid *OAuth2 Key* and *OAuth2 Secret*.
These can be obtained through the `Google Cloud Console`_.

    .. _Google Cloud Console: https://console.cloud.google.com/


Restricting Login
-----------------

Login can be restricted to a specific domain.
In *credentials.py* add all domains you want to
allow to :const:`SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS`
separated by commas.