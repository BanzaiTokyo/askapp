# Django based discussion board and a Q&amp;A system

## Run project in Docker
The easiest way to check out askapp is to run it's dockerized version:
- make sure you have Docker installed
- run `docker-compose up` from the project folder
This will run the project available at http://localhost:8000. 
It already has an admin user "askapp" with password "askapp"

## Steps to deploy a project:
- git clone https://github.com/BanzaiTokyo/askapp.git <project_dir>
- cd <project_dir>
- sudo pip -r requirements.txt
- create .env file with your credentials of format VARIABLE_NAME=VALUE. See list of variables below.
- create database in MySQL
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py collectstatic
- add a cron job `python manage.py calculate_scores` daily or hourly

## Enabling login with Google
Go to https://console.developers.google.com/, create a new project
Go to "Credentials" on left side menu, create new via "OAuth Client ID" option,
specify site root url (http://127.0.0.1:8000 for local or Docker installation ) 
for "Authorized Javascript origins" and (http://127.0.0.1:8000/accounts/google/login/callback/)
for "Authorized redirect URL".
Go to site admin -> "social accounts" -> "social applications", open or create social 
application named Google, add "client id" and "secret key" obtained from Google Oauth client.
Add site to "chosen sites", save changes.

## Environment variables:
```DJANGO_SECRET - any random string, a secret key used internally by Django security mechanisms
DB_HOST - database hostname
DB_NAME - database name
DB_USER, DB_PASSWORD - MySQL credentials
DB_PASSWORD - database user password
EMAIL_HOST - SMTP server address
EMAIL_ADDRESS, EMAIL_HOST_PASSWORD - SMTP credentials
GOOGLE_API_KEY - a key for Youtube API to pull description for Youtube videos
RECAPTCHA_PRIVATE_KEY and RECAPTCHA_PUBLIC_KEY - Google reCaptcha's secret/site keys. Read more at https://www.google.com/recaptcha/admin
GOOGLE_ANALYTICS_ID - optional, Google Analytics ID to collect site statistics
```

### How to get Google API Key
There are numerous tutorials how to do that, for example
https://www.slickremix.com/docs/get-api-key-for-youtube/ or https://www.yotuwp.com/how-to-get-youtube-api-key/


## Peculiarities when deploying to a Django instance from Bitnami hosted on AWS
- DB_HOST is /opt/bitnami/mysql/tmp/mysql.sock, DB_USER=root, DB_PASSWORD is taken from https://docs.bitnami.com/aws/faq/get-started/find-credentials/
- python executable is named "python3" there
- cron job may look like "0  *  * * *   bitnami /bin/bash -c '. $HOME/.profile; python3 manage.py calculate_scores'"

#### Additional steps:
- cp ../Project/conf ./
- sed -i 's|Project/Project|<project_dir>/askapp|g' *
- sed -i 's|Project|<project_dir>|g' *
- sed -i 's|wsgi-djangostack |wsgi-djangostack user=bitnami group=bitnami|' conf/httpd-app.conf
- sudo echo Include \"$(readlink -f conf/httpd-prefix.conf)\" >> ~/stack/apache2/conf/bitnami/bitnami-apps-prefix.conf
- sudo /opt/bitnami/ctlscript.sh restart apache
- mkdir askapp/media
- sudo chmod 755 askapp/media
- mkdir -p /var/tmp/askapp_cache
