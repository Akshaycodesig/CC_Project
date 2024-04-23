FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt .

# Install Flask and pika
RUN pip install --no-cache-dir Flask pika

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "python","app.py" ]