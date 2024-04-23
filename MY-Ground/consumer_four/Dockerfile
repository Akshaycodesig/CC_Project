FROM python:3.8-slim-buster

WORKDIR /usr/src/app


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY order_processing.py order_processing.py

CMD ["python3", "order_processing.py"]