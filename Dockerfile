FROM python:3.6

ENV RUN_MODE release

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD exec gunicorn digisvn.wsgi:application --bind 0.0.0.0:8000 --workers 4
