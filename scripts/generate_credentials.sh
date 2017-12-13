#!/usr/bin/env bash

PROJECT_ROOT=$1

# make a copy of credentials.py.template
#cp ${PROJECT_ROOT}/helpdesk/helpdesk/credentials.py.template ${PROJECT_ROOT}/helpdesk/helpdesk/credentials.py

read -p "Setup Google OAuth2? " -n 1 -r
echo    # move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    read -r -p "Enter Google OAuth2 API Key: " api_key
    read -r -p "Enter Google OAuth2 API Secret: " api_secret
    read -r -p "Enter Domains to Whitelist: " domain_whitelist
fi

read -p "Setup Email Server Credentials? " -n 1 -r
echo    # move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    read -r -p "Enter Email Server Username: " email_user
    read -r -p "Enter Email Server Password: " email_password
    read -r -p "Enter Email Host Address: " email_host
    read -r -p "Email users TLS? " -n 1
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        use_tls="True"
    else
        use_tls="False"
    fi
fi