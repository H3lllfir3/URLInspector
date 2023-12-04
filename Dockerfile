FROM python:3.11-bullseye

WORKDIR /app


RUN apt-get update && apt-get install -y cron

COPY requirements.txt .
RUN pip install -r requirements.txt


ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY . .
RUN python3 setup.py install

ENTRYPOINT [ "inspector" ]
