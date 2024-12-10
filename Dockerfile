FROM python:slim

RUN apt-get update \
    && apt-get -y install ffmpeg libavcodec-extra

RUN pip install pydub watchdog mutagen python-dotenv

WORKDIR /app

COPY app/ .

ENTRYPOINT python monitor.py
