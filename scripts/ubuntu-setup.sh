#!/usr/bin/env bash

# install apache2, sqlite, python3, pip, git
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib apache2 \
                        libapache2-mod-wsgi-py3 sqlite git

# clone repo
git clone https://gitlab.com/winstc/helpdesk.git

# project root
HELPDESK_ROOT=$(pwd)/helpdesk

# cd into repo
cd ${HELPDESK_ROOT}

# install python virtualenv
pip3 install virtualenv

# setup python virtualenv and activate it
mkdir ${HELPDESK_ROOT}/helpdeskenv/
virtualenv ${HELPDESK_ROOT}/helpdeskenv/
source  ${HELPDESK_ROOT}/helpdeskenv/bin/activate

# install python requirements
pip3 install -r pip-requirements.txt

# generate a secret key for django
${HELPDESK_ROOT}/helpdesk/manage.py generate_secret_key  --replace

# create secret_key.txt and make it read only
chmod 440 ${HELPDESK_ROOT}/helpdesk/secretkey.txt

# generate password for postgres
postgres_passwd=$(openssl rand -base64 32)

# setup postgres db
scripts/database_setup.sh $postgres_passwd

# update postgres password in credentials.py
sed -i.bkp -e "s/\${password}/$postgres_passwd/" credentials.py

# migrate django database
${HELPDESK_ROOT}/helpdesk/manage.py makemigrations
${HELPDESK_ROOT}/helpdesk/manage.py migrate

# collect static files
${HELPDESK_ROOT}/helpdesk/manage.py collectstatic

# make superuser
${HELPDESK_ROOT}/helpdesk/manage.py createsuperuser

##### Setup Apache #####

# generate apache conf
${HELPDESK_ROOT}/scripts/generate_apache_conf.sh $HELPDESK_ROOT

# move apache conf
cp ${HELPDESK_ROOT}/apache-conf/000-default /etc/apache2/sites-available/

# change ownership of static file dirs
sudo chown :www-data /var/www/html/media/uploads

# restart apache
sudo systemctl restart apache2.service

echo "Setup Complete!"
