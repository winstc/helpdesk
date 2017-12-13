#!/usr/bin/env bash


su - postgres <<EOSU
psql postgres -c "CREATE DATABASE helpdesk;"

psql postgres -c "CREATE USER helpdeskuser WITH PASSWORD '$1';"

passwrd=""

psql postgres -c "ALTER ROLE helpdeskuser SET client_encoding TO 'utf8';"
psql postgres -c "ALTER ROLE helpdeskuser SET default_transaction_isolation TO 'read committed';"
psql postgres -c "ALTER ROLE helpdeskuser SET timezone TO 'UTC';"

psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE helpdesk TO helpdeskuser;"

EOSU