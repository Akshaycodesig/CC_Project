FROM python:3.8-slim-buster

WORKDIR /usr/src/app


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY stock_management.py stock_management.py
COPY stock_view.py stock_view.py

CMD ["sh", "-c", "python3 stock_management.py && python3 stock_view.py"]