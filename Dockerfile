FROM ubuntu:20.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Kolkata \
    apt-get install -y \
    libpq-dev \
    python3-dev \
    espeak \
    ffmpeg \
    mbrola \
    mbrola-us1 \
    mbrola-us2 \
    python3 \
    python3-pip && \
    apt-get clean

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput

CMD gunicorn spoken_tut.wsgi:application --bind 0.0.0.0:8765