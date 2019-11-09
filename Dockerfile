FROM python:3.8.0-alpine

RUN apk --no-cache add ca-certificates git bash vim openssl gcc build-base make musl-dev python3-dev libffi-dev openssl-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/src/app/src

RUN  \
    mkdir config &&\
    openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout config/myKey.pem -out config/myCrt.pem -subj "/C=ES/ST=BCN/L=BCN/O=myapp.api/CN=myapp.api.com"

RUN \
    python migrate.py db init &&\
    python migrate.py db migrate &&\
    python migrate.py db upgrade

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src"

EXPOSE 8080

CMD [ "python", "run.py" ]
