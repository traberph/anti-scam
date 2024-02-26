from python:3.12-bookworm

WORKDIR /app

COPY req.txt req.txt
COPY pwd.csv pwd.csv
COPY send.py send.py

RUN pip install -r req.txt

CMD ["python3", "send.py"]