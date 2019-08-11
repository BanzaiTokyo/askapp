# Django based discussion board and a Q&amp;A system

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

## Environment variables:
```DJANGO_SECRET - any random string, a secret key used internally by Django security mechanisms
DB_HOST - database hostname
DB_DATABASE - database name
DB_USER, DB_PASSWORD - MySQL credentials
DB_PASSWORD - database user password
EMAIL_HOST - SMTP server address
EMAIL_ADDRESS, EMAIL_HOST_PASSWORD - SMTP credentials```

## Peculiarities when deploying to a Django instance from Bitnami hosted on AWS
- DB_HOST is /opt/bitnami/mysql/tmp/mysql.sock, DB_USER=root, DB_PASSWORD is taken from https://docs.bitnami.com/aws/faq/get-started/find-credentials/
- python executable is named "python3" there

#### Additional steps:
- cp ../Project/conf ./
- sed -i 's|Project/Project|<project_dir>/askapp' *
- sed -i 's|Project|<project_dir>' *
- sudo echo Include \"$(readlink -f conf/httpd-prefix.conf)\" >> ~/stack/apache2/conf/bitnami/bitnami-apps-prefix.conf
- sudo /opt/bitnami/ctlscript.sh restart apache
- mkdir askapp/media
- sudo chown daemon:daemon -R askapp/media
- sudo chmod 755 askapp/media
- mkdir -p /var/tmp/askapp_cache && sudo chown daemon:daemon /var/tmp/askapp_cache