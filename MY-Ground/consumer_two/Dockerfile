FROM python:3.8-slim-buster

WORKDIR /usr/src/app


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY item_creation.py item_creation.py

CMD ["python3", "item_creation.py"]