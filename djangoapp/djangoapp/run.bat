@echo off
claa venv\scripts\activate
python manage.py runserver_plus 0.0.0.0:403 --cert-file certs/cert.pem --key-file certs/key.pem > out.log 2>&1