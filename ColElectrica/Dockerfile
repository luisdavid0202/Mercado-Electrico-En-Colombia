FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

RUN apk --update add bash nano

COPY ./requirements.txt /var/www/requirements.txt

RUN apk update && apk add \
    gcc \
    g++

RUN pip install --upgrade pip \
    && pip install Brotli \
    && pip install -r /var/www/requirements.txt

EXPOSE 4500

COPY ./ColElectrica /ColElectrica

WORKDIR /ColElectrica

CMD ["python", "ColElectrica.py"]