#!/usr/bin/env bash

HELPDESK_ROOT=$1
TEMPLATE_DIR=${HELPDESK_ROOT}/apache-conf
TEMPLATE=${TEMPLATE_DIR}/000-default.conf

# make a copy of conf template
cp ${TEMPLATE_DIR}/000-default.conf.template ${TEMPLATE}

static_dir=/var/www/html/static
media_dir=/var/www/html/media
python_path=${HELPDESK_ROOT}/helpdesk
python_home=${HELPDESK_ROOT}/helpdeskenv
wsgi_dir=${HELPDESK_ROOT}/helpdesk/helpdesk
wsgi_script=${wsgi_dir}/wsgi.py

sed -i -e "s#\${static_dir}#$static_dir#g" \
       -e "s#\${media_dir}#$media_dir#g" \
       -e "s#\${python_path}#$python_path#g" \
       -e "s#\${python_home}#$python_home#g" \
       -e "s#\${wsgi_dir}#$wsgi_dir#g" \
       -e "s#\${wsgi_script}#$wsgi_script#g" ${TEMPLATE}
