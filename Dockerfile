FROM python:3.8.2-alpine

RUN apk update && apk add --no-cache --virtual build-deps build-base gcc g++ musl-dev libc-dev libffi-dev && \
    apk add mariadb-dev linux-headers openssh-client git && \
    pip install mysqlclient && \
    apk add jpeg-dev zlib-dev libjpeg

WORKDIR /code
ADD requirements.txt /code
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del build-deps

ADD . /code

EXPOSE 8000

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD /wait && python manage.py runserver 0.0.0.0:8000
