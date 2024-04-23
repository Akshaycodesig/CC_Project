FROM python:3.8-slim-buster

WORKDIR /usr/src/app


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY healthcheck.py healthcheck.py

CMD ["python3", "healthcheck.py"]