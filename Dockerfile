FROM python:3.11-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Set the Python path
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY . .
RUN python setup.py install

ENTRYPOINT [ "inspector" ]
